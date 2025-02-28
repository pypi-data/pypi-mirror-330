import platform
import subprocess
import pathlib
import logging
from ...llm import LLMAPIClient
from ..prompt_editor.prompt_editor import PromptEditor

class ShellController:
    def __init__(self, llm_model="claude-3-5-sonnet-20241022"):
        self.os_type = platform.system().lower()  # 'windows' または 'linux'
        file_path = pathlib.Path(__file__).parent / "shell_controller_prompt.txt"
        self.prompt_editor = PromptEditor(file_path)
        self.client = LLMAPIClient(model=llm_model)

    def execute_order(self, order):
        """オーダーを実行する"""
        commands = self.create_commands(order)
        results = []
        for command in commands:
            result = self.execute_command(command)
            results.append({"command": command, "result": result})
        return results

    def create_commands(self, order):
        """シェルコマンドを作成する"""
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
        """単一のシェルコマンドを実行する

        Args:
            command (dict): 実行するコマンド
                {"command": "実行するコマンド文字列", "shell": True/False}

        Returns:
            dict: 実行結果
                {
                    "stdout": 標準出力の文字列,
                    "stderr": 標準エラー出力の文字列,
                    "return_code": 終了コード
                }
        """
        if not isinstance(command, dict):
            raise ValueError("コマンドは辞書形式である必要があります")

        cmd = command.get("command")
        if not cmd:
            raise ValueError("commandキーが必要です")

        use_shell = command.get("shell", True)

        try:
            process = subprocess.Popen(
                cmd,
                shell=use_shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            return {
                "stdout": stdout,
                "stderr": stderr,
                "return_code": process.returncode
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }