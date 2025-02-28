import json
import logging
import re

class JsonParseError(Exception):
    """JSONパース時のカスタムエラー"""
    def __init__(self, message: str, original_response: str, original_error: Exception | None = None):
        self.message = message
        self.original_response = original_response
        self.original_error = original_error
        super().__init__(self.message)

class JsonConverter:
    def convert_json_string_to_dict(self, llm_json: str) -> dict | list:
        content = self._extract_code_block("json", llm_json)
        if not content:
            content = llm_json  # コードブロックがない場合、全体を使用
            # 最初の { または [ の左側と最後の } または ] の右側を削除
            content = re.sub(r'^[^{\[]*', '', content)  # 一番左の { または [ より左を削除
            content = re.sub(r'[^}\]]*$', '', content)  # 一番右の } または ] より右を削除
            content = content.strip()  # 余分な空白を削除
        try:
            llm_response = json.loads(content)
            logging.info(f"json解析に成功しました。\ncontent:{llm_response}")
        except json.JSONDecodeError as e:
            logging.error(f"""Error: json解析に失敗しました。
            error:{e}
            content:{llm_json}""")
            raise JsonParseError(
                message=f"LLMのレスポンスからJSONを解析できませんでした: {str(e)}",
                original_response=llm_json,
                original_error=e
            )
        
        return llm_response

    def _extract_code_block(self, language: str, text: str) -> str:
        pattern = fr"```{language}\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return ""