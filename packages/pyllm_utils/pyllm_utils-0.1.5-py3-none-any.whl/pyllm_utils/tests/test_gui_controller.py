import inspect
import logging
from llm.utils.gui_controller.gui_controller import NormalGUIController

def log_test_response(response):
    """テストレスポンスをログに記録する補助関数"""
    current_function = inspect.currentframe().f_back.f_code.co_name
    logging.info(f"Test: {current_function} - Response: {response}")

def test_gui_controller():
    controller = NormalGUIController()
    controller.execute_order("ゴミ箱を開ける")
    log_test_response(controller.execute_order("ゴミ箱を開ける"))