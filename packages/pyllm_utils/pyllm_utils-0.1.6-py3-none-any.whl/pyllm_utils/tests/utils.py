import logging
import inspect
from llm.utils.text_splitter import TokenBasedSplitter
from llm.utils.prompt_editor import PromptEditor
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

def test_text_splitter():
    text = "こんにちは、世界！"
    splitter = TokenBasedSplitter(
        min_chunk_tokens=20,
        max_chunk_tokens=100,
        min_sentences_per_chunk=3,
        similarity_threshold=0.7
    )
    chunks = splitter.split(text)
    log_test_response(chunks)

def test_prompt_editor():
    import pathlib
    template_source = pathlib.Path(__file__).parent / "test_prompt.txt"
    editor = PromptEditor(template_source)
    log_test_response(editor.processed_template)