from openai import OpenAI
import copy
import logging
import json
import sys
import pathlib
from .openai_message_converter import OpenAIMessageConverter
from ..common_converter.data_encoder import DataEncoder
from ..common_converter.json_converter import JsonConverter, JsonParseError
from ..common_converter.json_stream_converter import JsonStreamConverter
from .openai_chat_history_manager import OpenAIChatHistoryManager
        
class OpenAIClient:
    def __init__(self,
                 messages: list[dict[str, any]] | None = None, # type: ignore
                 model: str = "gpt-4o-mini",
                 store: bool | None = None,
                 metadata: dict[str, any] | None = None, # type: ignore
                 frequency_penalty: float | None = None,
                 logit_bias: dict[int, float] | None = None,
                 logprobs: bool | None = None,
                 top_logprobs: int | None = None,
                 max_tokens: int | None = None,
                 max_total_tokens: int | None = None,
                 max_completion_tokens: int | None = None,
                 n: int = 1,
                 modalities: list[str] | None = None,
                 audio: dict[str, str] | None = None,
                 use_audio_transcript: bool = True,
                 play_audio: bool = False,
                 presence_penalty: float | None = None,
                 response_format: dict | None = None,
                 seed: int | None = None,
                 service_tier: str | None = None,
                 stop: str | list[str] | None = None,
                 stream: bool | None = None,
                 stream_options: dict | None = None,
                 json_mode: bool | None = None,
                 stream_keys: list[str] | None = None,
                 temperature: float | None = None,
                 top_p: float | None = None,
                 tools: list[dict] | None = None,
                 tool_object: object | None = None,
                 tool_choice: str | dict | None = None,
                 parallel_tool_calls: bool | None = None,
                 user: str | None = None,
                 **kwargs):

        self.client = OpenAI()
        self.message_converter = OpenAIMessageConverter()
        self.data_encoder = DataEncoder()
        self.json_converter = JsonConverter()
        self.json_stream_converter = JsonStreamConverter()
        self.messages: list[dict] = messages if messages else []
        self.kwargs = {}
        
        # 明示的に定義された引数のリストを取得
        self.defined_params = set(self.__init__.__code__.co_varnames[:self.__init__.__code__.co_argcount])
        
        # パラメータの処理
        init_params = {
            key: value for key, value in locals().items()
            if key not in ["self", "kwargs"] 
            and key in self.defined_params
            and value is not None
        }
        self.kwargs.update(init_params)
        
        # kwargsの中の未定義パラメータをチェック
        for key in kwargs:
            if key not in self.defined_params:
                logging.warning(f"Parameter '{key}' is not defined in OpenAI model parameters and will be ignored")
        
        if not max_total_tokens:
            with open(pathlib.Path(__file__).parent.parent / "models" / "models.json", "r", encoding="utf-8") as f:
                models_json = json.load(f)
            for model_info in models_json["openai"]:
                if model_info["name"] == model:
                    defined_max_tokens = model_info["context_window"]
        self.chat_history_manager = OpenAIChatHistoryManager(defined_max_tokens, model)
        self.processed_messages: list[dict] = []
        self.processed_tool_messages: list[dict] = []
        self.tool_called = False
        self.latest_complete_response = None
        self.json_stream = False
        self.json_non_stream = False
        self.normal_stream = False
        self.normal_non_stream = False
    
    def request_messages(self, chat=False, **kwargs):
        self.processed_messages = []
        self.processed_tool_messages = []
        self.tool_called = False
        new_kwargs = copy.deepcopy(self.kwargs)
        
        # kwargsの値で更新
        for key, value in kwargs.items():
            if key not in self.defined_params:
                logging.warning(f"Parameter '{key}' is not defined in OpenAI model parameters and will be ignored")
                continue
            new_kwargs[key] = value

        # 特別なパラメータを先に取得して削除
        use_audio_transcript = new_kwargs.pop("use_audio_transcript", True)
        play_audio = new_kwargs.pop("play_audio", False)
        tool_object = new_kwargs.pop("tool_object", None)
        json_mode = new_kwargs.pop("json_mode", False)
        stream_keys = new_kwargs.pop("stream_keys", None)
        max_total_tokens = new_kwargs.pop("max_total_tokens", None)
        
        # メッセージの変換
        new_kwargs["messages"] = self.message_converter.convert_request_messages(
            new_kwargs["messages"], 
            use_audio_transcript
        )

        if new_kwargs.get("stream", None):
            response_generator = self._process_stream_response(tool_object, chat, **new_kwargs)
            if json_mode:
                if not stream_keys:
                    raise ValueError("stream json mode needs stream_keys")
                json_response_generator = self.json_stream_converter.stream_json_values(response_generator, stream_keys)
                self._change_latest_flag(json_mode, True)
                return json_response_generator
            self._change_latest_flag(json_mode, True)
            return response_generator
        else:
            response_messages = self._process_non_stream_response(tool_object, **new_kwargs)
            all_json_messages = []
            for response_message in response_messages:
                if play_audio:
                    for message in response_message:
                        for content in message.get("content", []):
                            self.data_encoder.play_audio(content.get("audio", {}).get("content", None))
                            logging.info(f"Audio played")
                if json_mode:
                    json_messages = []
                    first_flag = True
                    for message in response_message:
                        for content in message.get("content", []):
                            response_json = self._try_json_parse(content.get("text", content.get("refusal", "")))
                            json_messages.append(response_json)
                            if first_flag:
                                first_response_json = response_json
                            first_flag = False
                    all_json_messages.append(json_messages)
            if json_mode:
                self._change_latest_flag(json_mode, False)
                self.latest_complete_response = all_json_messages
                return first_response_json
            else:
                self._change_latest_flag(json_mode, False)
                self.latest_complete_response = response_messages
                contents = response_messages[0][-1].get("content", [{}])
                if chat:
                    self.messages.extend(response_messages[0])
                return contents[0].get("text", contents[-1].get("refusal", "")) if isinstance(contents[-1], dict) else contents[-1]
    
    def _try_json_parse(self, content_text: str):
        try:
            return self.json_converter.convert_json_string_to_dict(content_text)
        except JsonParseError as e:
            messages = self._create_json_parse_error_message(e)
            response_json = self.request_messages(messages=messages, stream=False, json_mode=True)
            return response_json
    
    def _create_json_parse_error_message(self, e: JsonParseError):
        messages = [
            {"role": "system",
             "content": f"""以下にuserが示したJSONはパースに失敗したものです。正しくパースできるようにJSONを修正して、修正済みのJSONを返してください。
             その際、あなたの返答に修正後のJSON以外の返答は含めないようにして、JSONのみ返すようにしてください。"""},
            {"role": "user",
             "content": f"JSONのパースに失敗しました。\nJSON: {e.original_response}\nerror: {e.original_error}"}
        ]
        return messages

    def request_chat(self,
                     system_message: str | None = None,
                     user_message: list[dict] | str | None = None,
                     images: list[dict] | None = None,
                     detail: str = "high",
                     audios: dict[str, str] | None = None,
                     videos: list[dict] | None = None,
                     **kwargs): # type: ignore
        """
        This function is used to request a chat completion from the OpenAI API.

        Args:
            system_message (str | None, optional): The system message to be used in the chat completion. Defaults to None.
            user_message (list[dict] | str | None, optional): The user message to be used in the chat completion. Defaults to None.
            images (list[dict] | None, optional): The images to be used in the chat completion. Defaults to None.
            ex) [{"url" : "https://example.com/image.png"}, {"path": "path/to/image.png"}]
            audio (dict[str, str] | None, optional): The audio to be used in the chat completion. Defaults to None.
            ex) [{"url" : "https://example.com/audio.mp3"}, {"path": "path/to/audio.mp3"}]
            videos (list[dict] | None, optional): The videos to be used in the chat completion. Defaults to None.
            ex) [{"url" : "https://example.com/video.mp4"}, {"path": "path/to/video.mp4"}]

        Returns:
            _type_: _description_
        """
        new_kwargs = copy.deepcopy(self.kwargs)
        
        # kwargsの値で更新
        for key, value in kwargs.items():
            if key not in self.defined_params:
                logging.warning(f"Parameter '{key}' is not defined in OpenAI model parameters and will be ignored")
                continue
            new_kwargs[key] = value

        new_kwargs["messages"] = self.messages

        if system_message:
            new_kwargs["messages"] = [msg for msg in new_kwargs["messages"] if msg.get("role") != "system"]
            new_kwargs["messages"].insert(0, {"role": "system", "content": system_message})
        
        additional_content = []
        if user_message:
            additional_content.append({"type": "text", "text": user_message})
        
        if (not user_message) and (not system_message):
            new_kwargs["messages"] = self.messages

        if images:
            for image in images:
                if image.get("path", None):
                    additional_content.append({
                        "type": "image",
                        "image": {
                            "type": "path",
                            "content": image.get("path", ""),
                            "detail": detail
                        }
                    })
                elif image.get("url", None):
                    additional_content.append({
                        "type": "image",
                        "image": {
                            "type": "url",
                            "content": image.get("url", ""),
                            "detail": detail
                        }
                    })
                elif image.get("base64", None):
                    additional_content.append({
                        "type": "image",
                        "image": {
                            "type": "base64",
                            "content": image.get("base64", ""),
                            "detail": detail
                        }
                    })
            
        if audios:
            for audio in audios:
                audio_format = audio.get("content", "").split(".")[-1]
                if audio.get("path", None):
                    additional_content.append({
                        "type": "audio",
                        "audio": {
                            "type": "path",
                            "content": audio.get("path", ""),
                            "format": audio_format
                        }
                    })
                elif audio.get("url", None):
                    additional_content.append({
                        "type": "audio",
                        "audio": {
                            "type": "url",
                            "content": audio.get("url", ""),
                            "format": audio_format
                        }
                    })
        
        new_kwargs["messages"].append({"role": "user", "content": additional_content})

        new_kwargs["messages"] = self.chat_history_manager.adjust_messages_length(new_kwargs["messages"])
        self.messages = new_kwargs["messages"]
        response = self.request_messages(chat=True, **new_kwargs)
        return response
    
    def get_latest_response(self):
        if self.json_stream:
            content = self.processed_messages[-1].get("content", f"{{error: JSON mode is enabled but no response was generated}}")
            content_text = content[0].get("text", content[0].get("refusal", "")) if isinstance(content, list) else content
            json_response = self._try_json_parse(content_text)
            self.latest_complete_response = json_response
        elif self.normal_stream:
            self.latest_complete_response = [self.processed_messages]
        return self.latest_complete_response
    
    def clear_chat_history(self):
        self.messages = []

    def request_embeddings(self, input: str, model: str = "text-embedding-3-small"):
        assert model in ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
        try:
            return self.client.embeddings.create(input=input, model=model).data[0].embedding
        except APIError as e:
            logging.error(f"Error requesting embeddings: {e}")
            raise APIError(f"Error requesting embeddings: {e}")

    async def async_request_embeddings(self, input: str, model: str = "text-embedding-3-small"):
        return self.request_embeddings(input, model)

    def _process_non_stream_response(self, tool_object: object | None, **kwargs):
        new_kwargs = copy.deepcopy(kwargs)
        response = self._get_response_from_api_by_kwargs(**new_kwargs)
        responses = []
        for choice_number in range(new_kwargs["n"]):
            response_messages, tool_called = self._handle_non_stream_response(
                response,
                choice_number,
                new_kwargs.get("tools", None),
                tool_object
            )
            if tool_called:
                new_kwargs = self._delete_tools_from_kwargs(new_kwargs)
                new_kwargs["messages"].extend(response_messages)
                tool_response_messages, tool_called = self._handle_non_stream_response(
                    self._get_response_from_api_by_kwargs(**new_kwargs),
                    choice_number,
                    None,
                    None
                )
                response_messages.extend(tool_response_messages)
            else:
                pass
            responses.append(response_messages)
        return responses

    def _process_stream_response(self, tool_object: object | None, chat: bool = False, **kwargs):
        self.processed_messages = []
        new_kwargs = copy.deepcopy(kwargs)
        new_kwargs["n"] = 1
        response = self._get_response_from_api_by_kwargs(**new_kwargs)
        response_generator = self._handle_stream_response(
            response,
            new_kwargs.get("tools", None),
            tool_object,
            chat
        )
        return self._process_generator(response_generator, chat, **new_kwargs)

    def _process_generator(self, generator, chat, **kwargs):
        def stream_generator():
            nonlocal generator, chat, kwargs
            for chunk in generator:
                if not self.tool_called:
                    yield chunk
                else:
                    new_kwargs = copy.deepcopy(kwargs)
                    new_kwargs["messages"].extend(self.processed_messages)
                    new_kwargs = self._delete_tools_from_kwargs(new_kwargs)
                    tool_response_generator = self._handle_stream_response(
                        self._get_response_from_api_by_kwargs(**new_kwargs),
                        None,
                        None,
                        chat
                    )
                    for tool_chunk in tool_response_generator:
                        yield tool_chunk
            if chat:
                self.messages.extend(self.processed_messages)
        
        for chunk in stream_generator():
            yield chunk
        
        return stream_generator()
                
    def _handle_non_stream_response(self, 
                                    response, 
                                    choice_number: int, 
                                    tools: list[dict] | None = None, 
                                    tool_object: object | None = None): 
        response_message = self._get_choice_number_message(response, choice_number)
        converted_message = self.message_converter.convert_response_message(response_message)
        converted_messages = [converted_message]
        
        if converted_message.get("tool_calls", None):
            tool_call_messages = self._process_tool_calls(converted_message["tool_calls"], tools, tool_object)
            converted_messages.extend(tool_call_messages)
            tool_called = True
        else:
            tool_called = False
        
        return converted_messages, tool_called

    def _handle_stream_response(self,
                                response, 
                                tools: list[dict] | None, 
                                tool_object: object | None,
                                chat: bool = False):
        current_message: dict[str, any] = { # type: ignore
            "role": "assistant",
            "content": None,
            "tool_calls": []
        }
        current_tool_call = None
        
        # ジェネレーターの内容を保持しながら新しいジェネレーターを返す
        def stream_generator():
            nonlocal current_message, current_tool_call, tool_object, tools
            
            # 元のジェネレーターの内容をすべて処理
            for chunk in response:
                delta = self._get_delta(chunk)
                
                # コンテンツの処理
                delta_content = self._get_delta_content(delta)
                if delta_content is not None:
                    current_message["role"] = "assistant"
                    if current_message.get("content") == None:
                        current_message["content"] = [
                            {
                                "type": "text",
                                "text": ""
                            }
                        ]
                    current_message["content"][0]["text"] += delta_content
                    yield delta_content
                    sys.stdout.flush()
                
                # ツールコールの処理
                delta_tool_calls = self._get_delta_tool_calls(delta)
                if delta_tool_calls:
                    self.tool_called = True
                    current_message["role"] = "assistant"
                    for tool_call in delta_tool_calls:
                        if current_tool_call is None or tool_call.index != current_tool_call["index"]:
                            current_tool_call = {
                                "index": self._get_tool_call_index(tool_call),
                                "id": self._get_tool_call_id(tool_call),
                                "type": "function",
                                "function": {
                                    "name": "",
                                    "arguments": ""
                                }
                            }
                            current_message["tool_calls"].append(current_tool_call)
                        
                        if self._get_tool_call_function_name(tool_call):
                            current_tool_call["function"]["name"] = self._get_tool_call_function_name(tool_call)
                        if self._get_tool_call_function_arguments(tool_call):
                            current_tool_call["function"]["arguments"] += self._get_tool_call_function_arguments(tool_call)

            # すべての処理が完了した後にメッセージを追加
            self.processed_messages.append(current_message)
            if current_message.get("tool_calls", None):
                self.processed_tool_messages = self._process_tool_calls(current_message.get("tool_calls", None), tools, tool_object)
                self.processed_messages.extend(self.processed_tool_messages)
                self.tool_called = True
            else:
                self.tool_called = False
                self.processed_tool_messages = []
            yield ""
        return stream_generator()
                
    
    def _process_tool_calls(self, 
                            tool_calls: list[dict], 
                            tools: list[dict] | None = None, 
                            tool_object: object | None = None):
        if not tool_object:
            raise ValueError("Tool object is not provided")
        if not tool_calls:
            raise ValueError("Tool calls are not provided")
        if not tools:
            raise ValueError("Tools are not provided")
        
        tool_call_messages = []
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            if function_name in [tool["function"]["name"] for tool in tools]:
                try:
                    tool = getattr(tool_object, function_name)
                    if callable(tool):
                        tool_call_message = {}
                        tool_call_message["role"] = "tool"
                        # JSON文字列を辞書に変換
                        arguments = json.loads(tool_call["function"]["arguments"]) if isinstance(tool_call["function"]["arguments"], str) else tool_call["function"]["arguments"]
                        result = tool(**arguments)
                        tool_call_message["content"] = str(result) if result is not None else f"{function_name} was executed with arguments {arguments}."
                        tool_call_message["tool_call_id"] = tool_call["id"]
                        tool_call_messages.append(tool_call_message)
                        logging.info(f"Tool '{function_name}' was executed with arguments {arguments}.")
                    else:
                        logging.error(f"Tool '{function_name}' is not callable")
                except AttributeError:
                    logging.error(f"Tool '{function_name}' not found in tool_object")
                except TypeError as e:
                    logging.error(f"Invalid arguments for tool '{function_name}': {str(e)}")
                except Exception as e:
                    logging.error(f"Error executing tool '{function_name}': {str(e)}")
        
        return tool_call_messages  

    def _change_latest_flag(self, json_mode: bool, stream: bool):
        if json_mode and stream:
            self.json_stream = True
            self.normal_stream = False
            self.json_non_stream = False
            self.normal_non_stream = False
        elif json_mode and not stream:
            self.json_non_stream = True
            self.normal_stream = False
            self.normal_non_stream = False
            self.json_stream = False
        elif not json_mode and stream:
            self.normal_stream = True
            self.json_stream = False
            self.json_non_stream = False
            self.normal_non_stream = False
        else:
            self.normal_non_stream = True
            self.normal_stream = False
            self.json_stream = False
            self.json_non_stream = False
            
    def _get_response_from_api_by_kwargs(self, **kwargs):
        new_kwargs = copy.deepcopy(kwargs)
        try:
            return self.client.chat.completions.create(**new_kwargs)
        except APIError as e:
            logging.error(f"Error requesting messages: {e}")
            raise APIError(f"Error requesting messages: {e}")

    def _delete_tools_from_kwargs(self, kwargs: dict):
        kwargs.pop("tool_choice", None)
        return kwargs
    
    def _get_choice_number_message(self, response, choice_number: int):
        return response.choices[choice_number].message
    
    def _get_delta(self, chunk):
        return chunk.choices[0].delta
    
    def _get_delta_content(self, delta):
        return delta.content
    
    def _get_delta_tool_calls(self, delta):
        return delta.tool_calls

    def _get_tool_call_id(self, tool_call):
        return tool_call.id
    
    def _get_tool_call_function_name(self, tool_call):
        return tool_call.function.name
    
    def _get_tool_call_function_arguments(self, tool_call):
        return tool_call.function.arguments
    
    def _get_tool_call_index(self, tool_call):
        return tool_call.index

class APIError(Exception):
    """
    APIエラーを表す例外クラス
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
