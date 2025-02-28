import pytest
import base64
import logging
import inspect
from llm.gemini_api.gemini_client import GeminiClient
from test_utils.test_llm import judge_authenticity
from unittest.mock import MagicMock
import pathlib
import json
from PIL import Image
from io import BytesIO
# ロギングの設定
logging.basicConfig(
    filename='test_llm_responses.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s' 
)

class Tool:
    def add_two_numbers(self, a: int, b: int) -> int:
        return a + b
    
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_two_numbers",
            "description": "2つの数値を足し合わせる関数",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "1つ目の数値"},
                    "b": {"type": "number", "description": "2つ目の数値"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

def log_test_response(response):
    """テストレスポンスをログに記録する補助関数"""
    current_function = inspect.currentframe().f_back.f_code.co_name
    logging.info(f"Test: {current_function} - Response: {response}")

def test_request_messages_with_user_image_local_path():
    client = GeminiClient()
    # PosixPathをstr型に変換
    image_path = str(pathlib.Path(__file__).parent.parent.resolve() / 'test.png')
    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': 'この画像は何の画像ですか？'
                },
                {
                    'type': 'image',
                    'image': {
                        'type': 'path',
                        'content': image_path, 
                        'detail': 'high'
                    }
                }
            ]
        }
    ]
    response = client.request_messages(messages=messages)
    log_test_response(response)
    correct, reason = judge_authenticity("猫の画像に関することが書かれていれば正解です。", response)
    assert correct, reason

def test_request_messages_with_user_image_url():
    client = GeminiClient()
    url = "https://th.bing.com/th/id/OIP.fyKxvsr3bvoNud-A5Ij2fAHaE6?w=271&h=180&c=7&r=0&o=5&pid=1.7"
    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': 'この画像は何の画像ですか？'
                },
                {
                    'type': 'image',
                    'image': {
                        'type': 'url',
                        'content': url
                    }
                }
            ]
        }
    ]
    response = client.request_messages(messages=messages)
    log_test_response(response)
    correct, reason = judge_authenticity("猫の画像に関することが書かれていれば正解です。", response)
    assert correct, reason
    
def test_request_messages_with_user_video_local_path():
    client = GeminiClient()
    video_path = str(pathlib.Path(__file__).parent.resolve() / 'test_datas' / 'test.mp4')
    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'video',
                    'video': {
                        'type': 'path',
                        'content': video_path
                    }
                },
                {
                    'type': 'text',
                    'text': 'この動画は何の動画ですか？'
                }
            ]
        }
    ]
    response = client.request_messages(messages=messages)
    log_test_response(response)
    correct, reason = judge_authenticity("動画の内容が書かれていれば正解です。", response)
    assert correct, reason

def test_request_messages_with_user_image_base64():
    client = GeminiClient()
    file_path = str(pathlib.Path(__file__).parent.parent.resolve() / 'test.png')
    with open(file_path, 'rb') as file:
        image_data = base64.b64encode(file.read()).decode('utf-8')
    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': 'この画像は何の画像ですか？'
                },
                {
                    'type': 'image',
                    'image': {
                        'type': 'base64',
                        'content': image_data
                    }
                }
            ]
        }
    ]
    response = client.request_messages(messages=messages)
    log_test_response(response)
    correct, reason = judge_authenticity("猫の画像に関することが書かれていれば正解です。", response)
    assert correct, reason

def test_request_messages_with_assistant_tool_calls():
    client = GeminiClient()
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_two_numbers",
                "description": "2つの数値を足し合わせる関数",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "1つ目の数値"
                        },
                        "b": {
                            "type": "number",
                            "description": "2つ目の数値"
                        }
                    }
                }
            }
        }
    ]
    messages = [
        {
            'role': 'user',
            'content': '2と3を足し合わせてください。'
        }
    ]
    response = client.request_messages(messages=messages, tools=tools, tool_choice="auto", tool_object=Tool())
    log_test_response(response)
    correct, reason = judge_authenticity("2と3を足し合わせた結果が書かれていれば正解です。", response)
    assert correct, reason

def test_request_messages_audio():
    client = GeminiClient()
    audio_path = str(pathlib.Path(__file__).parent.resolve() / 'test_datas' / 'test.mp3')
    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type':'audio',
                    'audio': {
                        'type': 'path',
                        'content': audio_path,
                        'format': 'mp3'
                    }
                },
                {
                    'type':'text',
                    'text': 'どのような音源が含まれていますか？'
                }
            ]
        }
    ]
    response = client.request_messages(
        model="gemini-1.5-flash", 
        modalities=["text", "audio"],  # テキストとオーディオの両方を要求
        audio={"voice": "alloy", "format": "wav"},
        messages=messages
    )
    
    # オーディオ応答の処理
    response = client.get_latest_response()
    
    correct, reason = judge_authenticity("音声の内容が書かれているか、音声が識別できないことが書かれているかのどちらかがあれば正解です。", response)
    assert correct, reason

def test_stream_response_messages():
    client = GeminiClient()
    response_generator = client.request_messages(messages=[{'role': 'user', 'content': 'こんにちは、世界！'}], stream=True)
    for response in response_generator:
        pass
    response = client.get_latest_response()
    log_test_response(response)
    assert len(response) == 1

def test_stream_response_messages_with_tool_calls():
    client = GeminiClient()
    response_generator = client.request_messages(model="gemini-1.5-pro", messages=[{'role': 'user', 'content': '2と3を足し合わせてください。また3と4を足し合わせてください。'}], tools=tools, tool_choice="auto", stream=True, tool_object=Tool())
    for response in response_generator:
        pass
    response = client.get_latest_response()
    log_test_response(response)
    correct, reason = judge_authenticity("2と3を足し合わせた結果と3と4を足し合わせた結果が書かれていれば正解です。", str(response[0][-1]["content"]))
    assert correct, reason

def test_stream_json_response_with_tool_calls_and_response_keys():
    client = GeminiClient()
    response_generator = client.request_messages(messages=[{'role': 'user', 'content': 'responseキーにadd_two_numbersを使って3+4を計算してJSONを出力してください。'}], tools=tools, tool_choice="auto", stream=True, tool_object=Tool(), json_mode=True, stream_keys=["response"])
    for response in response_generator:
        pass
    json_response = client.get_latest_response()
    assert json_response == {"response": 7}