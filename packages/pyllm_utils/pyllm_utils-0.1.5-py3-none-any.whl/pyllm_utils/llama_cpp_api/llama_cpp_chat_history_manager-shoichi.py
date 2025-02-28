import base64
import requests  # type: ignore
import os
import tiktoken # type: ignore
import pathlib
import json
from math import ceil
from typing import Tuple
from PIL import Image
from io import BytesIO

class LlamaCppTokenCounter():
    def __init__(self, 
                 model: str ,
                 tools: list[dict] | None = None,
                 initial_message_tokens: int = 3, 
                 additional_message_tokens: int = 4):
        self.model = model
        self.tools = tools
        self.initial_message_tokens = initial_message_tokens
        self.additional_message_tokens = additional_message_tokens
        
    def count_tokens(self, text: str) -> int:
        if self.model.startswith("gpt-4o"): 
            return len(tiktoken.get_encoding("o200k_base").encode(text))
        else:
            return len(tiktoken.get_encoding("cl100k_base").encode(text))

    def count_messages_tokens(self, messages: list[dict]) -> int:
        total_tokens = self.initial_message_tokens + self.count_tokens(f"{self.tools}")
        
        for message in messages:
            total_tokens += self._process_message(message)
        
        return total_tokens

    def _process_message(self, message: dict) -> int:
        tokens = 0
        
        if content := message.get("content"):
            tokens += self._process_content(content)
        elif tool_calls := message.get("tool_calls"):
            tokens += self._process_tool_calls(tool_calls)
        
        return tokens

    def _process_content(self, content: list[dict] | str) -> int:
        if isinstance(content, list):
            return sum(self._process_content_item(item) for item in content)
        return self.count_tokens(content) + self.additional_message_tokens

    def _process_content_item(self, content: dict) -> int:
        content_type = content["type"]
        
        if content_type == "text":
            return self.count_tokens(content["text"]) + self.additional_message_tokens
        elif content_type == "refusal":
            return self.count_tokens(content["refusal"]) + self.additional_message_tokens
        elif content_type == "image":
            return self.process_image_content(content["image"]) + self.additional_message_tokens
        elif content_type == "audio":
            return 10000 + self.additional_message_tokens
        return 0

    def process_image_content(self, image: dict) -> int:
        detail = image.get("detail", "high")
        width, height = self._get_image_dimensions(image)
        
        if detail == "high":
            return self._calculate_high_res_image_tokens(width, height)
        return 85

    def _process_tool_calls(self, tool_calls: list[dict]) -> int:
        return sum(self.count_tokens(str(tool_call["function"])) + self.additional_message_tokens 
                  for tool_call in tool_calls)

    def _calculate_tiles(self, width: int, height: int) -> int:
        """画像サイズからタイル数を計算
        
        Args:
            width: 画像の幅
            height: 画像の高さ
            
        Returns:
            int: 必要なタイル数
        """
        # 2048x2048以内にリサイズ
        if width > 2048 or height > 2048:
            aspect_ratio = width / height
            if width > height:
                width = 2048
                height = int(width / aspect_ratio)
            else:
                height = 2048
                width = int(height * aspect_ratio)

        # 最短辺を768にリサイズ
        if width < height:
            scale = 768 / width
        else:
            scale = 768 / height
        
        scaled_width = int(width * scale)
        scaled_height = int(height * scale)
        
        # 512x512タイルの数を計算
        tiles_x = ceil(scaled_width / 512)
        tiles_y = ceil(scaled_height / 512)
        
        return tiles_x * tiles_y

    def _calculate_high_res_image_tokens(self, width: int, height: int) -> int:
        """高解像度画像のトークン数を計算
        
        Args:
            width: 画像の幅
            height: 画像の高さ
            
        Returns:
            int: トークン数
        """
        BASE_TOKENS = 85
        TOKENS_PER_TILE = 170
        tiles = self._calculate_tiles(width, height)
        return BASE_TOKENS + (TOKENS_PER_TILE * tiles)

    def _get_image_dimensions(self, image_data: dict) -> Tuple[int, int]:
        """画像のサイズを取得
        
        Args:
            image_data: 画像データ（path、url、またはbase64）を含む辞書
            
        Returns:
            Tuple[int, int]: (width, height)
        """
        image_type = image_data["type"]
        
        try:
            if image_type == "path":
                with Image.open(image_data["path"]) as img:
                    return img.size
                    
            elif image_type == "url":
                response = requests.get(image_data["url"])
                response.raise_for_status()
                with Image.open(BytesIO(response.content)) as img:
                    return img.size
                    
            elif image_type == "base64":
                # base64文字列をデコード
                image_bytes = base64.b64decode(image_data["base64"])
                with Image.open(BytesIO(image_bytes)) as img:
                    return img.size
                    
            else:
                raise ValueError(f"Unsupported image type: {image_type}")
                
        except Exception as e:
            # エラー時はデフォルトの最大サイズを返す
            print(f"Error getting image dimensions: {e}")
            return (2048, 2048)

class LlamaCppChatHistoryManager():
    def __init__(self, 
                 defined_max_tokens: int,
                 model: str,
                 messages: list[dict] | None = None, 
                 tools: list[dict] | None = None, 
                 initial_message_tokens: int = 3, 
                 additional_message_tokens: int = 4):
        
        self.token_counter = LlamaCppTokenCounter(model, tools, initial_message_tokens, additional_message_tokens)
        self.model = model
        with open(pathlib.Path(__file__).parent.parent / "models" / "models.json", "r", encoding="utf-8") as f:
            models_json = json.load(f)
        
        self.defined_max_tokens = defined_max_tokens
        for model_info in models_json["openai"]:
            if model_info["name"] == self.model:
                self.max_output_tokens = model_info["max_output_tokens"]
                max_total_tokens = model_info["context_window"]
                break
        
        assert self.defined_max_tokens <= max_total_tokens, f"defined_max_tokens should be less than {max_total_tokens} if model is {self.model}"
        
        # メッセージがNoneの場合は空のリストを設定
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

        if tools is None:
            self.tools = []
        else:
            self.tools = tools

        self.initial_message_tokens = initial_message_tokens
        self.additional_message_tokens = additional_message_tokens
        self.messages_max_tokens = self.defined_max_tokens - self.max_output_tokens + 2

    def count_tokens(self, text: str) -> int:
        return self.token_counter.count_tokens(text)
    
    def count_messages_tokens(self, messages: list[dict]) -> int:
        return self.token_counter.count_messages_tokens(messages)
    
    def adjust_messages_length(self, messages: list[dict]) -> list[dict]:
        request_messages_total_tokens = self.count_messages_tokens(messages)
        if request_messages_total_tokens <= self.defined_max_tokens - self.max_output_tokens:
            return messages
        else:
            messages_max_tokens = self.defined_max_tokens - self.max_output_tokens
            tokens_list = []
            for message in messages:
                tokens_list.append(self.count_messages_tokens([message]))
            reversed_tokens_list = reversed(tokens_list.copy())
            for i, tokens in enumerate(reversed_tokens_list):
                if messages_max_tokens > tokens:
                    messages_max_tokens -= tokens
                else:
                    messages = messages[len(tokens_list)-i-1:]
                    break
            
            if isinstance(messages[0]["content"], list):
                contents = messages[0]["content"]
                contents = self._adjust_message_content(contents, messages_max_tokens)
                messages[0]["content"] = contents
            elif isinstance(messages[0]["content"], str):
                messages[0]["content"] = self._adjust_content_text(messages[0]["content"], messages_max_tokens)
            
            if messages[0].get("tool_calls"):
                messages[0]["tool_calls"] = self._adjust_tool_calls(messages[0]["tool_calls"], messages_max_tokens)
                
            return messages
        
    def _adjust_message_content(self, contents: list[dict], max_tokens: int) -> list[dict]:
        reversed_contents = list(reversed(contents.copy()))  # 修正後
        
        for i, content in enumerate(reversed_contents):
            if content["type"] == "text" or content["type"] == "refusal":
                if self.model.startswith("gpt-4o"):
                    encoded_message = tiktoken.get_encoding("o200k_base").encode(content[content["type"]])
                    if len(encoded_message) > max_tokens:
                        decoded_message = tiktoken.get_encoding("o200k_base").decode(encoded_message)[:max_tokens-4]
                        contents = contents[:len(contents)-i-1]
                        contents[len(contents)-i-1][content["type"]] = decoded_message
                        break
                    else:
                        max_tokens -= len(encoded_message)
                else:
                    encoded_message = tiktoken.get_encoding("cl100k_base").encode(content[content["type"]])
                    if len(encoded_message) > max_tokens:
                        decoded_message = tiktoken.get_encoding("cl100k_base").decode(encoded_message)[:max_tokens-4]
                        contents = contents[:len(contents)-i-1]
                        contents[len(contents)-i-1][content["type"]] = decoded_message
                        break
                    else:
                        max_tokens -= len(encoded_message)
                break
            elif content["type"] == "image":
                image_tokens = self.token_counter.process_image_content(content["image"])
                if image_tokens > max_tokens:
                    if content["image"].get("detail", "high") == "high" and image_tokens - max_tokens > 85:
                        contents = content[:len(content)-i-1]
                        contents[len(contents)-i-1]["image"]["detail"] = "low"
                    else:
                        contents = contents[:len(contents)-i-1]
                else:
                    max_tokens -= image_tokens
                    
            elif content["type"] == "audio":
                if 10000 > max_tokens:
                    contents = contents[:len(contents)-i-1]
                else:
                    max_tokens -= 10000
            
        return contents

    def _adjust_tool_calls(self, tool_calls: list[dict], max_tokens: int) -> list[dict]:
        reversed_tool_calls = list(reversed(tool_calls.copy()))
        for i, tool_call in enumerate(reversed_tool_calls):
            if self.count_tokens(str(tool_call["function"])) > max_tokens:
                tool_calls = tool_calls[:len(tool_calls)-i-1]
                break
            else:
                max_tokens -= self.count_tokens(str(tool_call["function"]))
        return tool_calls
    
    def _adjust_content_text(self, text: str, max_tokens: int) -> str:
        if self.model.startswith("gpt-4o"):
            encoded_text = tiktoken.get_encoding("o200k_base").encode(text)
            decoded_text = tiktoken.get_encoding("o200k_base").decode(encoded_text)[:max_tokens-4]
            return decoded_text
        else:
            encoded_text = tiktoken.get_encoding("cl100k_base").encode(text)
            decoded_text = tiktoken.get_encoding("cl100k_base").decode(encoded_text)[:max_tokens-4]
            return decoded_text