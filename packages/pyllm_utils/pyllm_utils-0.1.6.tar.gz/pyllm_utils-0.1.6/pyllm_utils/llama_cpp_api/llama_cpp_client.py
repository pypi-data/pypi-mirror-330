import llama_cpp
import copy
import logging
import json
import sys
import pathlib
from .llama_cpp_message_converter import LlamaCppMessageConverter
from ..common_converter.data_encoder import DataEncoder
from ..common_converter.json_converter import JsonConverter, JsonParseError
from ..common_converter.json_stream_converter import JsonStreamConverter
from .llama_cpp_chat_history_manager import LlamaCppChatHistoryManager
        
class LlamaCppClient:
    def __init__(self,
                 model: str,
                 messages: list[dict[str, any]] | None = None, # type: ignore
                 frequency_penalty: float | None = None,
                 logit_bias: dict[int, float] | None = None,
                 logprobs: bool | None = None,
                 top_logprobs: int | None = None,
                 grammar: str | None = None,
                 repeat_penalty: float = 1,
                 tfs_z: float = 1,
                 mirostat_mode: int = 0,
                 mirostat_tau: float = 5,
                 mirostat_eta: float = 0.1,
                 max_tokens: int | None = None,
                 max_completion_tokens: int | None = None,
                 presence_penalty: float | None = None,
                 response_format: dict | None = None,
                 service_tier: str | None = None,
                 stop: str | list[str] | None = None,
                 stream: bool | None = None,
                 json_mode: bool | None = None,
                 stream_keys: list[str] | None = None,
                 temperature: float | None = None,
                 top_p: float | None = None,
                 top_k: int | None = None,
                 min_p: float | None = None,
                 typical_p: float | None = None,
                 tools: list[dict] | None = None,
                 tool_object: object | None = None,
                 tool_choice: str | dict | None = None,
                 user: str | None = None,
                 n_gpu_layers: int = 0,
                 split_mode: int = None,  # LLAMA_SPLIT_MODE_LAYER
                 main_gpu: int = 0,
                 tensor_split: list[float] | None = None,
                 rpc_servers: str | None = None,
                 vocab_only: bool = False,
                 use_mmap: bool = True,
                 use_mlock: bool = False,
                 kv_overrides: dict[str, bool | int | float | str] | None = None,
                 seed: int | None = None,
                 max_total_tokens: int | None = None, #n_ctx
                 n_batch: int = 512,
                 n_ubatch: int = 512,
                 n_threads: int | None = None,
                 n_threads_batch: int | None = None,
                 rope_scaling_type: int | None = None,  # LLAMA_ROPE_SCALING_TYPE_UNSPECIFIED
                 pooling_type: int = None,  # LLAMA_POOLING_TYPE_UNSPECIFIED
                 rope_freq_base: float = 0.0,
                 rope_freq_scale: float = 0.0,
                 yarn_ext_factor: float = -1.0,
                 yarn_attn_factor: float = 1.0,
                 yarn_beta_fast: float = 32.0,
                 yarn_beta_slow: float = 1.0,
                 yarn_orig_ctx: int = 0,
                 logits_all: bool = False,
                 embedding: bool = False,
                 offload_kqv: bool = True,
                 flash_attn: bool = False,
                 last_n_tokens_size: int = 64,
                 lora_base: str | None = None,
                 lora_scale: float = 1,
                 lora_path: str | None = None,
                 numa: bool | int = False,
                 chat_format: str | None = None,
                 chat_handler: object | None = None,  # LlamaChatCompletionHandler
                 draft_model: object | None = None,  # LlamaDraftModel
                 tokenizer: object | None = None,  # BaseLlamaTokenizer
                 type_k: int | None = None,
                 type_v: int | None = None,
                 spm_infill: bool = False,
                 verbose: bool = True,
                 **kwargs):

        self.message_converter = LlamaCppMessageConverter()
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
                logging.warning(f"Parameter '{key}' is not defined in LlamaCpp model parameters and will be ignored")
        
        local_models_json_path = pathlib.Path(__file__).parent.parent / "models" / "local_models.json"
        with open(local_models_json_path, "r") as f:
            local_models_json = json.load(f)
        for model_info in local_models_json["local_models"]:
            if model_info["name"] == model:
                self.model_path = model_info["path"]
                break
        else:
            raise ValueError(f"Model '{model}' not found in local models")

        if not max_total_tokens:
            for model_info in local_models_json["local_models"]:
                if model_info["name"] == model:
                    defined_max_tokens = model_info["context_window"]
                    
        if not max_completion_tokens and not max_tokens:
            for model_info in local_models_json["local_models"]:
                if model_info["name"] == model:
                    local_max_tokens = model_info["max_output_tokens"]

        self.model_config_params = {
            "model_path": self.model_path,
            "n_gpu_layers": self.kwargs.get("n_gpu_layers", 0),
            "split_mode": self.kwargs.get("split_mode", llama_cpp.LLAMA_SPLIT_MODE_LAYER),
            "main_gpu": self.kwargs.get("main_gpu", 0),
            "tensor_split": self.kwargs.get("tensor_split", None),
            "rpc_servers": self.kwargs.get("rpc_servers", None),
            "vocab_only": self.kwargs.get("vocab_only", False),
            "use_mmap": self.kwargs.get("use_mmap", True),
            "use_mlock": self.kwargs.get("use_mlock", False),
            "kv_overrides": self.kwargs.get("kv_overrides", None),
            "seed": self.kwargs.get("seed", None),
            "n_ctx": defined_max_tokens,
            "n_batch": self.kwargs.get("n_batch", 512),
            "n_ubatch": self.kwargs.get("n_ubatch", 512),
            "n_threads": self.kwargs.get("n_threads", None),
            "n_threads_batch": self.kwargs.get("n_threads_batch", None),
            "rope_scaling_type": self.kwargs.get("rope_scaling_type", llama_cpp.LLAMA_ROPE_SCALING_TYPE_UNSPECIFIED),
            "pooling_type": self.kwargs.get("pooling_type", llama_cpp.LLAMA_POOLING_TYPE_UNSPECIFIED),
            "rope_freq_base": self.kwargs.get("rope_freq_base", 0),
            "rope_freq_scale": self.kwargs.get("rope_freq_scale", 0),
            "yarn_ext_factor": self.kwargs.get("yarn_ext_factor", -1),
            "yarn_attn_factor": self.kwargs.get("yarn_attn_factor", 1),
            "yarn_beta_fast": self.kwargs.get("yarn_beta_fast", 32),
            "yarn_beta_slow": self.kwargs.get("yarn_beta_slow", 1),
            "yarn_orig_ctx": self.kwargs.get("yarn_orig_ctx", 0),
            "logits_all": self.kwargs.get("logits_all", False),
            "embedding": self.kwargs.get("embedding", False),
            "offload_kqv": self.kwargs.get("offload_kqv", True),
            "flash_attn": self.kwargs.get("flash_attn", False),
            "last_n_tokens_size": self.kwargs.get("last_n_tokens_size", 64),
            "lora_base": self.kwargs.get("lora_base", None),
            "lora_scale": self.kwargs.get("lora_scale", 1),
            "lora_path": self.kwargs.get("lora_path", None),
            "numa": self.kwargs.get("numa", False),
            "chat_format": self.kwargs.get("chat_format", None),
            "chat_handler": self.kwargs.get("chat_handler", None),
            "draft_model": self.kwargs.get("draft_model", None),
            "tokenizer": self.kwargs.get("tokenizer", None),
            "type_k": self.kwargs.get("type_k", None),
            "type_v": self.kwargs.get("type_v", None),
            "spm_infill": self.kwargs.get("spm_infill", False),
            "verbose": self.kwargs.get("verbose", True),
        }

        self.generation_config_params = {
            "messages": self.messages,
            "tools": self.kwargs.get("tools", None),
            "tool_choice": self.kwargs.get("tool_choice", None),
            "tool_object": self.kwargs.get("tool_object", None),
            "temperature": self.kwargs.get("temperature", None),
            "top_p": self.kwargs.get("top_p", None),
            "top_k": self.kwargs.get("top_k", None),
            "min_p": self.kwargs.get("min_p", None),
            "typical_p": self.kwargs.get("typical_p", None),
            "stop": self.kwargs.get("stop", None),
            "seed": self.kwargs.get("seed", None),
            "response_format": self.kwargs.get("response_format", None),
            "max_tokens": self.kwargs.get("max_completion_tokens", self.kwargs.get("max_tokens", local_max_tokens)),
            "presence_penalty": self.kwargs.get("presence_penalty", None),
            "frequency_penalty": self.kwargs.get("frequency_penalty", None),
            "tfs_z": self.kwargs.get("tfs_z", None),
            "mirostat_mode": self.kwargs.get("mirostat_mode", None),
            "mirostat_tau": self.kwargs.get("mirostat_tau", None),
            "mirostat_eta": self.kwargs.get("mirostat_eta", None),
            "logits_processor": self.kwargs.get("logits_processor", None),
            "logprobs": self.kwargs.get("logprobs", None),
            "top_logprobs": self.kwargs.get("top_logprobs", None),
            "grammar": self.kwargs.get("grammar", None),
            "repeat_penalty": self.kwargs.get("repeat_penalty", None),
        }
        
        copied_model_config_params = copy.deepcopy(self.model_config_params)
        copied_model_config_params.pop("model_path", None)
        self.client = llama_cpp.Llama(model_path=self.model_path, **copied_model_config_params)
        self.chat_history_manager = LlamaCppChatHistoryManager(defined_max_tokens, model, self.client, self.messages, self.kwargs.get("tools", None))
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
                logging.warning(f"Parameter '{key}' is not defined in LlamaCpp model parameters and will be ignored")
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

    def request_chat(self,
                     system_message: str | None = None,
                     user_message: list[dict] | str | None = None,
                     images: list[dict] | None = None,
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
                logging.warning(f"Parameter '{key}' is not defined in LlamaCpp model parameters and will be ignored")
                continue
            new_kwargs[key] = value

        new_kwargs["messages"] = self.messages

        if system_message:
            new_kwargs["messages"] = [msg for msg in new_kwargs["messages"] if msg.get("role") != "system"]
            new_kwargs["messages"].insert(0, {"role": "system", "content": system_message})
        
        additional_content = []
        if user_message:
            additional_content.append({"role": "user", "content": user_message})
        
        if (not user_message) and (not system_message):
            new_kwargs["messages"] = self.messages

        if images:
            for image in images:
                if image.get("path", None):
                    additional_content.append(
                        {
                            "role": "user",
                            "content": {
                                "type": "image",
                                "image": {
                                    "type": "path",
                                    "content": image.get("path", ""),
                                }
                            }
                        }
                    )
                elif image.get("url", None):
                    additional_content.append(
                        {
                            "role": "user",
                            "content": {
                                "type": "image",
                                "image": {
                                    "type": "url",
                                    "content": image.get("url", ""),
                                }
                            }
                        }
                    )
        
        new_kwargs["messages"].extend(additional_content)

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

    def _process_non_stream_response(self, tool_object: object | None, **kwargs):
        new_kwargs = copy.deepcopy(kwargs)
        response = self._get_response_from_api_by_kwargs(**new_kwargs)
        responses = []
        new_kwargs["n"] = 1
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
        
        # ジェネレーターの内容を保持しながら新しいジ���ネレーターを返す
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
            
    def _create_generation_config_params(self, **kwargs):
        kwargs_copy = copy.deepcopy(kwargs)
        generation_config_params = {
            "messages": kwargs_copy.pop("messages", None),
            "tools": kwargs_copy.pop("tools", None),
            "tool_choice": kwargs_copy.pop("tool_choice", None),
            "tool_object": kwargs_copy.pop("tool_object", None),
            "temperature": kwargs_copy.pop("temperature", None),
            "top_p": kwargs_copy.pop("top_p", None),
            "top_k": kwargs_copy.pop("top_k", None),
            "min_p": kwargs_copy.pop("min_p", None),
            "typical_p": kwargs_copy.pop("typical_p", None),
            "stop": kwargs_copy.pop("stop", None),
            "seed": kwargs_copy.pop("seed", None),
            "response_format": kwargs_copy.pop("response_format", None),
            "max_tokens": kwargs_copy.pop("max_completion_tokens", kwargs_copy.pop("max_tokens", None)),
            "presence_penalty": kwargs_copy.pop("presence_penalty", None),
            "frequency_penalty": kwargs_copy.pop("frequency_penalty", None),
            "tfs_z": kwargs_copy.pop("tfs_z", None),
            "mirostat_mode": kwargs_copy.pop("mirostat_mode", None),
            "mirostat_tau": kwargs_copy.pop("mirostat_tau", None),
            "mirostat_eta": kwargs_copy.pop("mirostat_eta", None),
            "logits_processor": kwargs_copy.pop("logits_processor", None),
            "logprobs": kwargs_copy.pop("logprobs", None),
            "top_logprobs": kwargs_copy.pop("top_logprobs", None),
            "grammar": kwargs_copy.pop("grammar", None),
            "repeat_penalty": kwargs_copy.pop("repeat_penalty", None),
            "stream": kwargs_copy.pop("stream", None),
        }
        copied_generation_config_params = copy.deepcopy(generation_config_params)
        for key, value in copied_generation_config_params.items():
            if not value:
                generation_config_params.pop(key, None)
        return generation_config_params
            
    def _get_response_from_api_by_kwargs(self, **kwargs):
        new_kwargs = copy.deepcopy(kwargs)
        generation_config_params = self._create_generation_config_params(**new_kwargs)
        generation_config_params["messages"] = self.message_converter.convert_request_messages(
            generation_config_params["messages"], 
            generation_config_params.get("use_audio_transcript", True)
        )
        generation_config_params.pop("tool_object", None)
        logging.info(f"generation_config_params: {generation_config_params}")
        return self.client.create_chat_completion(**generation_config_params)
    
    def _get_choice_number_message(self, response, choice_number: int):
        return response.get("choices", [{}])[choice_number].get("message", None)
    
    def _get_delta(self, chunk):
        return chunk.get("choices", [{}])[0].get("delta", None)
    
    def _get_delta_content(self, delta):
        return delta.get("content", None)
    
    def _get_delta_tool_calls(self, delta):
        return delta.get("tool_calls", None)

    def _get_tool_call_id(self, tool_call):
        return tool_call.get("id", None)
    
    def _get_tool_call_function_name(self, tool_call):
        return tool_call.get("function", {}).get("name", None)
    
    def _get_tool_call_function_arguments(self, tool_call):
        return tool_call.get("function", {}).get("arguments", None)
    
    def _get_tool_call_index(self, tool_call):
        return tool_call.get("index", None)
