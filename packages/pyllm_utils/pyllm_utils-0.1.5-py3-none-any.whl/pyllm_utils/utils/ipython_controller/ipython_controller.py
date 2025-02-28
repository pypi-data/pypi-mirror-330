import platform
import pathlib
import logging
from IPython.core.interactiveshell import InteractiveShell
from ...llm import LLMAPIClient
from ..prompt_editor.prompt_editor import PromptEditor

class IPythonController:
    def __init__(self, llm_model="claude-3-5-sonnet-20241022"):
        self.os_type = platform.system().lower()
        file_path = pathlib.Path(__file__).parent / "ipython_controller_prompt.txt"
        self.prompt_editor = PromptEditor(file_path)
        self.client = LLMAPIClient(model=llm_model)
        # IPythonシェルの初期化
        self.shell = InteractiveShell.instance()

    def execute_order(self, order):
        """オーダーを実行する"""
        commands = self.create_commands(order)
        results = []
        for command in commands:
            result = self.execute_command(command)
            results.append({"command": command, "result": result})
        return results

    def create_commands(self, order):
        """IPythonコマンドを作成する"""
        prompt = self.prompt_editor.apply({
            "order": order,
            "os_type": self.os_type
        })
        try:
            response = self.client.request_messages(
                messages=[
                {"role": "user", "content": prompt},
                {"role": "user", "content": "Only return the JSON object, no other text or comments."}
            ], 
            json_mode=True)
        except Exception as e:
            logging.error(f"コマンドの作成に失敗しました: {e}")
            raise ValueError(f"コマンドの作成に失敗しました: {e}")
        return response

    def execute_command(self, command):
        """IPythonコマンドを実行する

        Args:
            command (dict): 実行するコマンド
                {
                    "code": "実行するコード",
                    "type": "code/magic/system"  # コードタイプ
                }

        Returns:
            dict: 実行結果
                {
                    "output": 実行結果,
                    "error": エラーメッセージ（存在する場合）,
                    "success": 成功したかどうか,
                    "display_data": 表示データ（画像などがある場合）
                }
        """
        if not isinstance(command, dict):
            raise ValueError("コマンドは辞書形式である必要があります")

        code = command.get("code")
        if not code:
            raise ValueError("codeキーが必要です")

        cmd_type = command.get("type", "code")

        try:
            if cmd_type == "system":
                # システムコマンド実行
                result = self.shell.system(code)
                return {
                    "output": result,
                    "error": None,
                    "success": True,
                    "display_data": None
                }
            elif cmd_type == "magic":
                # マジックコマンド実行
                result = self.shell.run_line_magic(code.lstrip('%'), '')
                return {
                    "output": result,
                    "error": None,
                    "success": True,
                    "display_data": None
                }
            else:
                # 通常のPythonコード実行
                result = self.shell.run_cell(code)
                return {
                    "output": result.result,
                    "error": result.error_in_exec if result.error_before_exec or result.error_in_exec else None,
                    "success": result.success,
                    "display_data": result.display_data
                }
        except Exception as e:
            return {
                "output": None,
                "error": str(e),
                "success": False,
                "display_data": None
            }