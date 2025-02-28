import pytest
import base64
import logging
import inspect
from llm.utils.img_pos_getter import ImagePosGetter

# ロギングの設定
logging.basicConfig(
    filename='test_llm_responses.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s' 
)

def log_test_response(response):
    """テストレスポンスをログに記録する補助関数"""
    current_function = inspect.currentframe().f_back.f_code.co_name
    logging.info(f"Test: {current_function} - Response: {response}")

def test_claude_get_img_pos():
    img_pos_getter = ImagePosGetter(model="claude-3-5-sonnet-20241022")
    img_pos = img_pos_getter.get_img_pos("ゴミ箱")
    log_test_response(img_pos)

def test_gemini_get_img_pos():
    img_pos_getter = ImagePosGetter(model="gemini-1.5-pro")
    img_pos = img_pos_getter.get_img_pos("ゴミ箱")
    log_test_response(img_pos)
    
def test_gemini_get_img_bbox():
    img_pos_getter = ImagePosGetter(model="gemini-1.5-pro")
    img_bbox = img_pos_getter.get_img_bbox("ゴミ箱")
    log_test_response(img_bbox)