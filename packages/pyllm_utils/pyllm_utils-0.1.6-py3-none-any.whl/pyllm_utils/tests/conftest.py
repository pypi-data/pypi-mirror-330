import pytest
import logging
import pathlib
from logging.handlers import RotatingFileHandler

@pytest.fixture(autouse=True)
def setup_logging():
    # ログファイルのパスを設定
    log_dir = pathlib.Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "test_llm_responses.log"

    # 既存のハンドラをクリア
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # RotatingFileHandlerを設定
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )

    # フォーマッタを設定（時刻のみ表示）
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    # ルートロガーの設定
    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(file_handler)

    yield  # テスト実行

    # テスト終了後にハンドラをクローズ
    file_handler.close()
    logging.root.removeHandler(file_handler)
