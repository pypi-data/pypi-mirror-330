import copy
import logging
import json
from ..common_converter.data_encoder import DataEncoder

class AnthropicMessageConverter():
    def __init__(self):
        self.ALL_TYPES = ["audio", "image", "video","file_uri", "mime_type", "language", "code", "outcome", "output"]
        self.data_encoder = DataEncoder()
        self.ALLOWED_TYPES = []
        self.ROLES = {
            "system": "user",
            "user": "user",
            "assistant": "assistant",
            "tool": "user",
            "model": "assistant"
        }
        self.previous_message = None
        self.previous_tool_calls_contents = []
        self.previous_tool_calls_length = 0
        
    def convert_request_messages(self, messages: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
        assert isinstance(messages, list) or messages is None, "messages must be a list or None"
        tmp_messages = copy.deepcopy(messages)
        if tmp_messages is None:
            logging.warning("messages is None")
            return []
        
        converted_messages = [self._process_request_message(message) for message in tmp_messages]
        reconverted_messages = [converted_message for converted_message in converted_messages if converted_message is not None]
        
        return reconverted_messages
    
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
        role = tmp_message.get("role", None)
        if tmp_message["role"] not in self.ROLES:
            logging.warning(f"Invalid role: {role}")
            raise ValueError(f"Invalid role: {role}")
        if tmp_message["role"] == "tool":
            if self.previous_tool_calls_length > 0:
                tmp_content = {"type": "tool_result", "tool_use_id": tmp_message.get("tool_call_id", None), "content": tmp_message.get("content", None)}
                tmp_message["content"] = [tmp_content]
                tmp_message["role"] = "user"
                self.previous_tool_calls_contents.append(tmp_content)
                self.previous_tool_calls_length -= 1
            if self.previous_tool_calls_length == 0:
                completed_tool_calls = copy.deepcopy(self.previous_tool_calls_contents)
                self.previous_tool_calls_contents = []
                tmp_message["role"] = "user"
                tmp_message["content"] = completed_tool_calls
                tmp_message.pop("tool_call_id")
                return tmp_message
            else:
                return None
                
        tmp_message["role"] = self.ROLES[role]
        
        if isinstance(tmp_message.get("content", None), list):
            tmp_message["content"] = [self._process_request_content(content) for content in tmp_message["content"]]
        elif isinstance(tmp_message.get("content", None), str):
            tmp_message["content"] = [{"type": "text", "text": tmp_message["content"]}]
        if isinstance(tmp_message.get("tool_calls", None), list):
            for tool_call in tmp_message["tool_calls"]:
                tool_dict: dict = {}
                tool_dict["id"] = tool_call.get("id", None)
                tool_dict["type"] = "tool_use"
                tool_dict["name"] = tool_call.get("function", {}).get("name", None)
                tool_dict["input"] = json.loads(tool_call.get("function", {}).get("arguments", None))
                if not tmp_message.get("content", None):
                    tmp_message["content"] = []
                tmp_message["content"].append(tool_dict)
            self.previous_tool_calls_length = len(tmp_message["tool_calls"])
            tmp_message.pop("tool_calls")
        return tmp_message
    
    def _process_request_content(self, content: dict) -> dict:
        tmp_content = copy.deepcopy(content)
        content_type = tmp_content["type"]
        if content_type in ["text", "refusal", "audio"]:
            if tmp_content.get("audio", {}).get("audio_transcript", None):
                tmp_content["text"] = tmp_content.get("audio", {}).get("audio_transcript", None)
            else:
                tmp_content["text"] = tmp_content.get("text", tmp_content.get("refusal", None))
            return tmp_content
        elif content_type == "image" and tmp_content.get("image", {}).get("type", None) == "path":
            tmp_content["type"] = "image"
            data, media_type = self.data_encoder.encode_image_path_to_normal_base64str_and_media_type(tmp_content.get("image", {}).get("content", "This local path is not found."))
            tmp_content["source"] = {
                "type": "base64",
                "media_type": media_type, 
                "data": data
            }
        elif content_type == "image" and tmp_content.get("image", {}).get("type", None) == "base64":
            tmp_content["type"] = "image"
            data, media_type = self.data_encoder.encode_image_base64_to_normal_base64str_and_media_type(tmp_content.get("image", {}).get("content", "This base64 data is not found."))
            tmp_content["source"] = {
                "type": "base64",
                "media_type": media_type,
                "data": data
            }
        elif content_type == "image" and tmp_content.get("image", {}).get("type", None) == "url":
            tmp_content["type"] = "image"
            data, media_type = self.data_encoder.encode_image_url_to_normal_base64str_and_media_type(tmp_content.get("image", {}).get("content", "This image url is not found."))
            tmp_content["source"] = {
                "type": "base64",
                "media_type": media_type,
                "data": data
            }
        elif content_type == "file_data":
            tmp_content["type"] = "text"
            tmp_content["text"] = f"```mime_type:\n{tmp_content.get('mime_type', 'This mime type is not found.')}\nfile data:\n{tmp_content.get('file_uri', 'This file uri is not found.')}\n```"
            logging.info(f"Converted file_data to text: {tmp_content['text']}")
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
        for key in ["image", "audio", "refusal",  "file_uri", "mime_type", "language", "code", "outcome", "output"]:
            tmp_content.pop(key, None)
        return tmp_content

    
    def _get_message_role(self, message) -> str:
        return message.role
    
    def _get_message_content(self, message) -> list[dict] | None:
        for content in message.content:
            if content.type == "text":
                return content.text
        return None

    def _get_message_refusal(self, message) -> None:
        return None

    def _get_message_audio(self, message) -> None:
        return None

    def _get_message_audio_id(self, audio) -> None:
        return None

    def _get_message_audio_data(self, audio) -> None:
        return None

    def _get_message_audio_transcript(self, audio) -> None:
        return None

    def _get_message_tool_calls(self, message) -> list[dict] | None:
        tool_calls = []
        for content in message.content:
            if content.type == "tool_use":
                tool_calls.append(content)
        if len(tool_calls) == 0:
            return None
        return tool_calls

    def _get_message_tool_call_id(self, tool_call) -> str:
        return tool_call.id

    def _get_message_tool_call_function(self, tool_call) -> dict:
        return tool_call

    def _get_message_tool_call_function_name(self, function) -> str:
        return function.name

    def _get_message_tool_call_function_arguments(self, function) -> str:
        return json.dumps(function.input)