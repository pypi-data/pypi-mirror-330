import inspect
import logging
from llm.utils.ipython_controller.ipython_controller import IpythonController

def log_test_response(response):
    """テストレスポンスをログに記録する補助関数"""
    current_function = inspect.currentframe().f_back.f_code.co_name
    logging.info(f"Test: {current_function} - Response: {response}")

def test_ipython_controller():
    controller = IpythonController()
    log_test_response(controller.execute_order("１～１０までの数字の和を計算してください。"))
