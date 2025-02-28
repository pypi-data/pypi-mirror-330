import inspect
import logging
from llm.utils.shell_controller.shell_controller import ShellController

def log_test_response(response):
    """テストレスポンスをログに記録する補助関数"""
    current_function = inspect.currentframe().f_back.f_code.co_name
    logging.info(f"Test: {current_function} - Response: {response}")

def test_shell_controller():
    controller = ShellController()
    log_test_response(controller.execute_order("今のディレクトリの中身を教えてください。"))
