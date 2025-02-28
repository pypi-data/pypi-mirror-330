import pathlib
import os
# X11認証の設定
os.environ['DISPLAY'] = ':1'
try:
    # まず/home/abc/.Xauthorityを試す
    xauth_path = '/config/.Xauthority'
    if not os.path.exists(xauth_path):
        # ディレクトリが存在することを確認
        os.makedirs('/config', exist_ok=True)
        # 空の.Xauthorityファイルを作成
        open(xauth_path, 'a').close()
    os.environ['XAUTHORITY'] = xauth_path
except Exception as e:
    print(f"X11認証の設定中にエラーが発生しました: {e}")

import pyautogui
# フェイルセーフを無効化（推奨されません）
pyautogui.FAILSAFE = False

# フェイルセーフのトリガー位置を変更（左上以外にする場合）
pyautogui.FAILSAFE_POINTS = [(0, 0), (0, 999), (999, 0), (999, 999)]  # 全ての画面の角をトリガーポイントに
import logging
import pathlib
import platform
import subprocess
from datetime import datetime
from ...llm import LLMAPIClient
from ..img_pos_getter.img_pos_getter import ImagePosGetter
from ..prompt_editor.prompt_editor import PromptEditor
from ..computer_use_demo.loop import sampling_loop
from ..computer_use_demo.loop import APIProvider
from ..callbacks.base_callback import BaseCallback

class ComputerUseGUIController:
    def __init__(self, computer_use_prompt: str = "computer_use_prompt", max_messages: int = 5):
        self.messages = []
        self.max_messages = max_messages
        computer_use_prompt_file_path = pathlib.Path(__file__).parent / "prompts" / "computer_use_prompt" / f"{computer_use_prompt}.txt"
        with open(computer_use_prompt_file_path, "r") as file:
            self.system_prompt = file.read()
        applied_prompt = {
            "platform_machine": platform.machine(),
            "datetime_today": datetime.today().strftime('%A, %B %-d, %Y')
        }
        self.computer_use_prompt_editor = PromptEditor(computer_use_prompt)
        self.computer_use_prompt = self.computer_use_prompt_editor.apply(applied_prompt)

    async def execute_order(self, 
                            order,
                            callbacks: BaseCallback = BaseCallback()):
        
        self.messages.append({"role": "user", "content": order})
        try:
            output = subprocess.check_output(['xrandr']).decode()
            # 現在の解像度を検索 (例: "1920x1080+0+0")
            for line in output.split('\n'):
                if '*' in line:  # アクティブな解像度を示す
                    resolution = line.split()[0]
                    width, height = resolution.split('x')
                    os.environ["WIDTH"] = width
                    os.environ["HEIGHT"] = height
                    break

        except (subprocess.CalledProcessError, FileNotFoundError):
            logging.error("解像度の取得に失敗しました")
            raise ValueError("解像度の取得に失敗しました")
        
        result = await sampling_loop(
            model="claude-3-5-sonnet-20241022",
            provider=APIProvider.ANTHROPIC,
            system_prompt=self.computer_use_prompt,
            messages=self.messages,
            output_callback=callbacks.computer_use_output_callback,
            tool_output_callback=callbacks.computer_use_tool_output_callback,
            api_response_callback=callbacks.computer_use_api_response_callback,
            api_key = os.environ["ANTHROPIC_API_KEY"]
        )
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        return result
    
    def set_callbacks(self, callbacks: BaseCallback):
        self.callbacks = callbacks
    
class NormalGUIController:
    def __init__(self, llm_model="claude-3-5-sonnet-20241022",image_pos_getter_model="claude-3-5-sonnet-20241022"):
        self.img_pos_getter = ImagePosGetter(model=image_pos_getter_model)
        file_path = pathlib.Path(__file__).parent / "gui_controller_prompt.txt"
        self.prompt_editor = PromptEditor(file_path)
        self.client = LLMAPIClient(model=llm_model)
        self.api_company = self.client.client

    def execute_order(self, order):
        """オーダーを実行する"""
        try:
            commands = self.create_commands(order)
            for command in commands:
                self.execute_command(command)
        except Exception as e:
            logging.error(f"オーダーの実行に失敗しました: {e}")
            raise ValueError(f"オーダーの実行に失敗しました: {e}")
        return commands
        
    def create_commands(self, order):
        """コマンドを作成する"""
        prompt =self.prompt_editor.apply({"order": order})
        if self.api_company == "google":
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
        else:
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
    
    def _get_coordinates(self, command):
        """コマンドから座標を取得する。object_nameが指定されている場合はImagePosGetterを使用"""
        try:
            if "object_name" in command:
                pos = self.img_pos_getter.get_img_pos(command["object_name"])
                if pos is None:
                    raise ValueError(f"画像が見つかりませんでした: {command['object_name']}")
                return pos["x"], pos["y"]
            return command.get("x"), command.get("y")
        except Exception as e:
            raise ValueError(f"座標の取得に失敗しました: {str(e)}")

    def execute_command(self, command):
        """単一のGUIコマンドを実行する

        Args:
            command (dict): 実行するコマンド
                move: {"move": {"object_name": name} or {"x": x, "y": y, "duration": duration}}
                click: {"click": {"object_name": name} or {"x": x, "y": y, "clicks": clicks, "interval": interval, "button": button}}
                right_click: {"right_click": {"object_name": name} or {"x": x, "y": y}}
                double_click: {"double_click": {"object_name": name} or {"x": x, "y": y, "interval": interval, "button": button}}
                write: {"write": {"text": text, "interval": interval}}
                press: {"press": {"key": key}}
                hotkey: {"hotkey": {"keys": [key1, key2, ...]}}
                drag: {"drag": {"object_name": name} or {"x": x, "y": y, "duration": duration, "button": button}}
                scroll: {"scroll": {"clicks": clicks, "object_name": name} or {"x": x, "y": y}}
                wait: {"wait": {"seconds": seconds}}
                middle_click: {"middle_click": {"object_name": name} or {"x": x, "y": y}}
        """
        if not isinstance(command, dict):
            raise ValueError("コマンドは辞書形式である必要があります")

        if command.get("move"):
            x, y = self._get_coordinates(command["move"])
            pyautogui.moveTo(
                x, y,
                duration=command["move"].get("duration", 0)
            )
        elif command.get("click"):
            x, y = self._get_coordinates(command["click"])
            pyautogui.click(
                x, y,
                clicks=command["click"].get("clicks", 1),
                interval=command["click"].get("interval", 0.0),
                button=command["click"].get("button", "left")
            )
        elif command.get("right_click"):
            x, y = self._get_coordinates(command["right_click"])
            pyautogui.rightClick(x, y)
        elif command.get("double_click"):
            x, y = self._get_coordinates(command["double_click"])
            pyautogui.doubleClick(
                x, y,
                interval=command["double_click"].get("interval", 0.0),
                button=command["double_click"].get("button", "left")
            )
        elif command.get("write"):
            pyautogui.write(
                command["write"]["text"],
                interval=command["write"].get("interval", 0.0)
            )
        elif command.get("press"):
            pyautogui.press(command["press"]["key"])
        elif command.get("hotkey"):
            pyautogui.hotkey(*command["hotkey"]["keys"])
        elif command.get("drag"):
            x, y = self._get_coordinates(command["drag"])
            pyautogui.dragTo(
                x, y, 
                duration=command["drag"].get("duration", 0.5),
                button=command["drag"].get("button", "left")
            )
        elif command.get("scroll"):
            x, y = self._get_coordinates(command["scroll"])
            pyautogui.scroll(
                command["scroll"]["clicks"],
                x=x,
                y=y
            )
        elif command.get("wait"):
            pyautogui.sleep(command["wait"]["seconds"])
        elif command.get("middle_click"):
            x, y = self._get_coordinates(command["middle_click"])
            pyautogui.middleClick(x, y)

    def set_callbacks(self, callbacks: BaseCallback):
        self.callbacks = callbacks
