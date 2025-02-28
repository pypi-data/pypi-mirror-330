import copy
import logging
from ..common_converter.data_encoder import DataEncoder # type: ignore

class LlamaCppMessageConverter():
    def __init__(self):
        self.ALL_TYPES = ["audio", "image", "video","file_uri", "mime_type", "language", "code", "outcome", "output"]
        self.data_encoder = DataEncoder()
        self.ALLOWED_TYPES = []
        self.ROLES = {
            "system": "system",
            "user": "user",
            "assistant": "assistant",
            "tool": "tool",
            "model": "assistant"
        }

    def convert_request_messages(self, messages: list[dict] | None = None, use_audio_transcript: bool = True) -> list[dict]:
        assert isinstance(messages, list) or messages is None, "messages must be a list or None"
        tmp_messages = copy.deepcopy(messages)
        if tmp_messages is None:
            logging.warning("messages is None")
            return []
        
        return [self._process_request_message(message, use_audio_transcript) for message in tmp_messages]

    def convert_response_message(self, message) -> dict: 
        converted_message: dict[str, list[dict] | str] = {}
        converted_message['role'] = self._get_message_role(message)
        converted_message['content'] = []
        message_content = self._get_message_content(message)
        if message_content:
            converted_message['content'].append({"type": "text", "text": message_content})

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
        return converted_message

    def _process_request_message(self, message: dict, use_audio_transcript: bool = True) -> dict:
        tmp_message = copy.deepcopy(message)
        
        if tmp_message["role"] not in self.ROLES:
            logging.warning(f"Invalid role: {tmp_message['role']}")
            raise ValueError(f"Invalid role: {tmp_message['role']}")
        tmp_message["role"] = self.ROLES[tmp_message["role"]]
        
        if isinstance(tmp_message["content"], list):
            tmp_message["content"] = [self._process_request_content(content, use_audio_transcript) for content in tmp_message["content"]]
        
        return tmp_message

    def _process_request_content(self, content: dict, use_audio_transcript: bool = True) -> dict:
        tmp_content = copy.deepcopy(content)
        content_type = tmp_content["type"]
        if content_type == "text":
            return tmp_content
        elif content_type == "refusal":
            tmp_content["type"] = "text"
            tmp_content["text"] = tmp_content.get("refusal", "This refusal is not found.")
            return tmp_content
        elif content_type == "audio":
            audio_info = tmp_content.get("audio", {})
            audio_type = audio_info.get("type", None)
            audio_transcript = audio_info.get("audio_transcript", None)
            audio_content = audio_info.get("content", "This audio content is not found.")
            
            if audio_transcript:
                tmp_content["type"] = "text"
                tmp_content["text"] = audio_transcript
            else:
                tmp_content["type"] = "text"
                tmp_content["text"] = "audio is not supported."

        elif content_type == "image" and tmp_content.get("image", {}).get("type", None) == "path":
            tmp_content["type"] = "image_url"
            tmp_content["image_url"] = {}
            tmp_content["image_url"]["url"] = self.data_encoder.encode_image_path_to_base64str(tmp_content.get("image", {}).get("content", "This local path is not found."))
            tmp_content["image_url"]["detail"] = tmp_content.get("image", {}).get("detail", "high")
        elif content_type == "image" and tmp_content.get("image", {}).get("type", None) == "base64":
            tmp_content["type"] = "image_url"
            tmp_content["image_url"] = {}
            tmp_content["image_url"]["url"] = self.data_encoder.encode_image_base64_to_base64str(tmp_content.get("image", {}).get("content", "This base64 data is not found."))
            tmp_content["image_url"]["detail"] = tmp_content.get("image", {}).get("detail", "high")
        elif content_type == "image" and tmp_content.get("image", {}).get("type", None) == "url":
            tmp_content["type"] = "image_url"
            tmp_content["image_url"] = {}
            tmp_content["image_url"]["url"] = tmp_content.get("image", {}).get("content", "This url is not found.")
            tmp_content["image_url"]["detail"] = tmp_content.get("image", {}).get("detail", "high")
        elif content_type == "video":
            tmp_content["type"] = "image_url"
            tmp_content["image_url"] = {}
            ## 途中
            return {"type": "text", "text": "video is not supported."}
        elif content_type == "file_data":
            tmp_content["type"] = "text"
            ##途中
            tmp_content["text"] = f"```mime_type:\n{tmp_content.get('mime_type', 'This mime type is not found.')}\nfile data:\n{tmp_content.get('file_uri', 'This file uri is not found.')}\n```"
            pass
        elif content_type == "executable_code":
            tmp_content["type"] = "text"
            tmp_content["text"] = f"```language:\n{tmp_content.get('language', 'This language is not found.')}\ncode:\n{tmp_content.get('code', 'This code is not found.')}\n```"
        elif content_type == "code_execution_result":
            tmp_content["type"] = "text"
            tmp_content["text"] = f"```code execution result:\n{tmp_content.get('outcome', 'This outcome is not found.')}\noutput:\n{tmp_content.get('output', 'This output is not found.')}\n```"
        else:
            logging.warning(f"Invalid content type: {content_type}")
            raise ValueError(f"Invalid content type: {content_type}")
        for key in ["audio", "image", "video", "file_uri", "mime_type", "language", "code", "outcome", "output"]:
            tmp_content.pop(key, None)
        return tmp_content

    def _get_message_role(self, message) -> str:
        return message.get("role", None)
    
    def _get_message_content(self, message) -> list[dict]:
        return message.get("content", None)

    def _get_message_refusal(self, message) -> str:
        return message.get("refusal", None)

    def _get_message_audio(self, message) -> dict:
        return message.get("audio", None)

    def _get_message_audio_id(self, audio) -> str:
        return audio.get("id", None)

    def _get_message_audio_data(self, audio) -> str:
        return audio.get("data", None)

    def _get_message_audio_transcript(self, audio) -> str:
        return audio.get("transcript", None)

    def _get_message_tool_calls(self, message) -> list[dict]:
        return message.get("tool_calls", None)

    def _get_message_tool_call_id(self, tool_call) -> str:
        return tool_call.get("id", None)

    def _get_message_tool_call_function(self, tool_call) -> dict:
        return tool_call.get("function", None)

    def _get_message_tool_call_function_name(self, function) -> str:
        return function.get("name", None)

    def _get_message_tool_call_function_arguments(self, function) -> str:
        return function.get("arguments", None)
