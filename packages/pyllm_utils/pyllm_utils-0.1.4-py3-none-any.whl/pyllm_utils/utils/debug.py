import logging
from typing import Union, Any

def log_dict_structure(
    data: Union[dict, list, Any],
    max_length: int = 50,
    indent: str = ""
) -> None:
    """
    辞書やリストの構造を階層的に表示する
    
    Args:
        data: 解析する辞書やリスト
        max_length: 値を表示する最大長
        indent: インデントレベル（再帰呼び出し用）
    """
    if isinstance(data, dict):
        logging.info(f"{indent}{{")  # 辞書の開始を表示
        for key, value in data.items():
            value_type = type(value).__name__
            if isinstance(value, (dict, list)):
                logging.info(f"{indent}  {key}: {value_type}")
                log_dict_structure(value, max_length, indent + "  ")
            else:
                try:
                    value_preview = str(value)
                    if len(value_preview) > max_length:
                        value_preview = f"{value_preview[:max_length]}... (length: {len(value_preview)})"
                except Exception:
                    value_preview = f"<{value_type}>"
                logging.info(f"{indent}  {key}: {value_preview}")
        logging.info(f"{indent}}}")  # 辞書の終了を表示
    elif isinstance(data, list):
        if data:
            logging.info(f"{indent}[")  # リストの開始を表示
            logging.info(f"{indent}  List of {len(data)} items:")
            log_dict_structure(data[0], max_length, indent + "  ")
            logging.info(f"{indent}]")  # リストの終了を表示
