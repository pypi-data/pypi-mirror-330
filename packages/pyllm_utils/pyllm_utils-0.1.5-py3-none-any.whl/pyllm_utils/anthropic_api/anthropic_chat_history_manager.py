import json
import pathlib
import copy
from anthropic import Anthropic
from .anthropic_message_converter import AnthropicMessageConverter
class AnthropicChatHistoryManager:
    def __init__(self, 
                 defined_max_tokens: int,
                 model: str,
                 messages: list[dict] | None = None,
                 tools: list[dict] | None = None,
                 tool_choice: str | None = None):
        
        self.token_counter = Anthropic().beta.messages
        self.model = model
        self.token_counter_kwargs = {
            "betas": ["token-counting-2024-11-01"],
            "model": self.model
        }
        with open(pathlib.Path(__file__).parent.parent / "models" / "models.json", "r", encoding="utf-8") as f:
            models_json = json.load(f)
        self.defined_max_tokens = defined_max_tokens
        for model_info in models_json["anthropic"]:
            if model_info["name"] == self.model:
                self.max_output_tokens = model_info["max_output_tokens"]
                max_total_tokens = model_info["context_window"]
                break
        
        assert self.defined_max_tokens <= max_total_tokens, f"defined_max_tokens should be less than {max_total_tokens} if model is {self.model}"
        
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

        if tools is None:
            self.tools = []
        else:
            self.tools = tools
        
        self.messages_max_tokens = self.defined_max_tokens - self.max_output_tokens
        self.message_converter = AnthropicMessageConverter()
        
    def count_messages_tokens(self, messages: list[dict], tools: list[dict] | None = None, tool_choice: str | None = None) -> int:
        copied_messages = copy.deepcopy(messages)
        converted_messages = self.message_converter.convert_request_messages(copied_messages)
        self.token_counter_kwargs["messages"] = converted_messages
        if tools is not None:
            self.token_counter_kwargs["tools"] = tools
        if tool_choice is not None:
            self.token_counter_kwargs["tool_choice"] = tool_choice
        return self.token_counter.count_tokens(**self.token_counter_kwargs).input_tokens

    def adjust_messages_length(self, messages: list[dict], tools: list[dict] | None = None, tool_choice: str | None = None) -> list[dict]:
        request_messages_total_tokens = self.count_messages_tokens(messages, tools, tool_choice)
        tokens_list = []
        for i, message in enumerate(messages):
            if i == 0:
                tokens = self.count_messages_tokens([message], tools, tool_choice)
                tokens_list.append(tokens)
            else:
                tokens = self.count_messages_tokens([message], tools, tool_choice) - tokens_list[i-1]
                tokens_list.append(tokens)
        reversed_tokens_list = reversed(tokens_list.copy())
        for i, tokens in enumerate(reversed_tokens_list):
            if request_messages_total_tokens > self.messages_max_tokens:
                request_messages_total_tokens -= tokens
            else:
                return messages[:len(tokens_list)-i]
            
        return messages
    
    