import copy
import logging
import json
import google.generativeai as genai # type: ignore
from ..common_converter.data_encoder import DataEncoder

class GeminiMessageConverter():
    def __init__(self):
        self.ALL_TYPES = ["audio", "image", "video", "file_uri", "mime_type", "language", "code", "outcome", "output"]
        self.data_encoder = DataEncoder()
        self.ALLOWED_TYPES = []
        self.ROLES = {
            "system": "user",
            "user": "user",
            "assistant": "model",
            "tool": "model",
            "model": "model"
        }

    def convert_request_messages(self, messages: list[dict[str, str]] | None = None, use_audio_transcript: bool = True) -> list[dict[str, str]]:
        assert isinstance(messages, list) or messages is None, "messages must be a list or None"
        tmp_messages = copy.deepcopy(messages)
        if tmp_messages is None:
            logging.warning("messages is None")
            return []
        
        converted_messages = [self._process_request_message(message, use_audio_transcript) for message in tmp_messages]
        return converted_messages

    def convert_response_message(self, message) -> dict: 
        converted_message: dict[str, list[dict] | str] = {}
        converted_message['role'] = self._get_message_role(message)
        converted_message['content'] = []
        message_content = self._get_message_content(message)
        if message_content:
            converted_message['content'].append({"type": "text", "text": message_content})
        message_refusal = self._get_message_refusal(message)
        if message_refusal:
            converted_message['content'].append({"type": "refusal", "refusal": message_refusal})
        message_audio = self._get_message_audio(message)
        if message_audio:
            # base64エンコードされたバイトデータをそのまま使用
            audio_id = self._get_message_audio_id(message_audio)
            audio_data = self._get_message_audio_data(message_audio)
            audio_transcript = self._get_message_audio_transcript(message_audio)
            converted_message['content'].append({
                "type": "audio", 
                "audio": {
                    "id": audio_id,
                    "type": "base64",
                    "content": audio_data.decode('utf-8') if isinstance(audio_data, bytes) else audio_data,
                    "audio_transcript": audio_transcript if audio_transcript else None
                }
            })

        message_tool_calls = self._get_message_tool_calls(message)
        if message_tool_calls:
            converted_message['tool_calls'] = []
            for tool_call in message_tool_calls:
                tool_call_id = self._get_message_tool_call_id(tool_call)
                tool_call_function = self._get_message_tool_call_function(tool_call)
                tool_call_function_name = self._get_message_tool_call_function_name(tool_call_function)
                tool_call_function_arguments = self._get_message_tool_call_function_arguments(tool_call_function)
                converted_message['tool_calls'].append({
                    "id": tool_call_id,
                    "type": "function",
                    "function": {
                        "name": tool_call_function_name,
                        "arguments": tool_call_function_arguments
                    }
                })

        message_tool_call_response = self._get_message_tool_call_response(message)
        if message_tool_call_response:
            converted_message["type"] = "text"
            converted_message['text'] = message_tool_call_response
        
        message_executable_code = self._get_message_executable_code(message)
        if message_executable_code:
            converted_message["type"] = "executable_code"
            converted_message['code'] = self._get_message_code(message_executable_code)
            converted_message['language'] = self._get_message_code_language(message_executable_code)
        message_code_execution_result = self._get_message_code_execution_result(message)
        if message_code_execution_result:
            converted_message["type"] = "code_execution_result"
            converted_message['outcome'] = self._get_message_code_execution_result_outcome(message_code_execution_result)
            converted_message['output'] = self._get_message_code_execution_result_output(message_code_execution_result)
        
        return converted_message
    
    def _process_request_message(self, message: dict, use_audio_transcript: bool = True) -> dict:
        tmp_message = copy.deepcopy(message)
        role = tmp_message.get("role", None)
        if tmp_message["role"] not in self.ROLES:
            logging.warning(f"Invalid role: {tmp_message['role']}")
            raise ValueError(f"Invalid role: {tmp_message['role']}")
        tmp_message["role"] = self.ROLES[tmp_message["role"]]
        
        if isinstance(tmp_message.get("content", None), list):
            tmp_message["parts"] = [self._process_request_content(content, use_audio_transcript) for content in tmp_message["content"]]
            tmp_message.pop("content")
        elif isinstance(tmp_message.get("content", None), str):
            tmp_message["parts"] = [tmp_message["content"]]
            tmp_message.pop("content")
        elif isinstance(tmp_message.get("tool_calls", None), list):
            tool_calls = []
            for tool_call in tmp_message["tool_calls"]:
                tool_dict: dict = {}
                tool_dict["function_call"] = {}
                tool_dict["function_call"]["name"] = tool_call.get("function", {}).get("name", None)
                tool_dict["function_call"]["args"] = tool_call.get("function", {}).get("arguments", None)
                tool_calls.append(tool_dict)
            tmp_message["parts"] = tool_calls
            tmp_message.pop("tool_calls")
        
        return tmp_message
    
    def _process_request_content(self, content: dict, use_audio_transcript: bool = True) -> dict | str:
        tmp_content = copy.deepcopy(content)
        content_type = tmp_content["type"]
        if content_type == "text":
            return tmp_content.get("text", "")
        elif content_type == "audio":
            audio_info = tmp_content.get("audio", {})
            audio_type = audio_info.get("type", None)
            audio_transcript = audio_info.get("audio_transcript", None)
            audio_content = audio_info.get("content", None)

            if use_audio_transcript and audio_transcript:
                tmp_content = audio_transcript
            else:
                tmp_content["mime_type"] = self.data_encoder.get_audio_mime_type(audio_content)
                if audio_type == "path":
                    tmp_content["data"] = self.data_encoder.encode_audio_path_to_base64(audio_content)
                elif audio_type == "url":
                    tmp_content["data"] = self.data_encoder.encode_audio_url_to_base64(audio_content)
                elif audio_type == "base64":
                    tmp_content["data"] = self.data_encoder.encode_audio_base64_to_base64str(audio_content)
        elif content_type == "refusal":
            tmp_content["text"] = f"```refusal:\n{tmp_content.get('refusal', 'This refusal is not found.')}\n```"
        elif content_type == "image" and tmp_content.get("image", None).get("type", None) == "path":
            tmp_content = self.data_encoder.encode_image_path_to_PIL(tmp_content.get("image", {}).get("content", "This local path is not found."))
        elif content_type == "image" and tmp_content.get("image", None).get("type", None) == "url":
            tmp_content = self.data_encoder.encode_image_url_to_PIL(tmp_content.get("image", {}).get("content", "This image url is not found."))
        elif content_type == "image" and tmp_content.get("image", None).get("type", None) == "base64":
            tmp_content = self.data_encoder.encode_image_base64_to_PIL(tmp_content.get("image", {}).get("content", "This base64 data is not found."))
        elif content_type == "video":
            tmp_content = self._upload_video_and_return_video_object(tmp_content.get("video", {}).get("content", "This video path is not found."))
        elif content_type == "file_data":
            tmp_content = self._upload_file_and_return_file_object(tmp_content.get("file_data", {}).get("content", "This file path is not found."))
        elif content_type == "executable_code":
            tmp_content = f"""\`\`\`{tmp_content.get("language", None)}\n{tmp_content.get("code", "This code is not found.")}\n\`\`\`"""
        elif content_type == "code_execution_result":
            tmp_content = tmp_content.get("output", "No output.")
        else:
            logging.warning(f"Invalid content type: {content_type}")
            raise ValueError(f"Invalid content type: {content_type}")
        for key in ["type","audio", "image", "file_uri"]:
            if isinstance(tmp_content, dict):
                tmp_content.pop(key, None)
                
        return tmp_content

    def _get_message_role(self, message) -> str:
        return message.role
    
    def _get_message_content(self, message) -> str:
        contents = message.parts
        for content in contents:
            if content.text:
                return content.text
        return ""
    
    def _get_message_refusal(self, message) -> str:
        return ""
    
    def _get_message_audio(self, message) -> dict:
        return {}

    def _get_message_audio_id(self, audio) -> str:
        return ""
    
    def _get_message_audio_data(self, audio) -> str:
        return ""

    def _get_message_audio_transcript(self, audio) -> str:
        return ""

    def _get_message_tool_calls(self, message) -> list[dict]:
        tool_calls = []
        for content in message.parts:
            if content.function_call:
                tool_calls.append(content.function_call)
        return tool_calls
    
    def _get_message_tool_call_id(self, tool_call) -> str:
        return ""
    
    def _get_message_tool_call_function(self, tool_call) -> dict:
        return tool_call
    
    def _get_message_tool_call_function_name(self, function) -> str:
        return function.name
    
    def _get_message_tool_call_function_arguments(self, function) -> str:
        arguments = {}
        for key, value in function.args.items():
            arguments[key] = value
            
        return json.dumps(arguments)
    
    def _get_message_tool_call_response(self, message):
        tool_call_response = {}
        for content in message.parts:
            if content.function_response:
                tool_call_response["name"] = content.function_response.name
                tool_call_response["response"] = content.function_response.response
        return tool_call_response
    
    def _get_message_executable_code(self, message):
        for content in message.parts:
            if content.executable_code:
                return content.executable_code
        return {}
    
    def _get_message_code(self, executable_code) -> str:
        return executable_code.code
    
    def _get_message_code_language(self, executable_code) -> str:
        return executable_code.outcome
    
    def _get_message_code_execution_result(self, message):
        for content in message.parts:
            if content.code_execution_result:
                return content.code_execution_result
        return {}
    
    def _get_message_code_execution_result_outcome(self, code_execution_result):
        return code_execution_result.outcome
    
    def _get_message_code_execution_result_output(self, code_execution_result) -> str:
        return code_execution_result.output
    
    def _upload_video_and_return_video_object(self, video_path: str):
        video_file = genai.upload_file(path=video_path)
        import time

        # Check whether the file is ready to be used.
        while video_file.state.name == "PROCESSING":
            logging.info("Uploading video...")
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            logging.error(f"Failed to upload video: {video_file.state.name}")
            raise ValueError(video_file.state.name)
        return video_file
    
    def _upload_file_and_return_file_object(self, file_path: str):
        file_object = genai.upload_file(path=file_path)
        import time
        while file_object.state.name == "PROCESSING":
            logging.info("Uploading file...")
            time.sleep(10)
            file_object = genai.get_file(file_object.name)

        if file_object.state.name == "FAILED":
            logging.error(f"Failed to upload file: {file_object.state.name}")
            raise ValueError(file_object.state.name)
        return file_object
