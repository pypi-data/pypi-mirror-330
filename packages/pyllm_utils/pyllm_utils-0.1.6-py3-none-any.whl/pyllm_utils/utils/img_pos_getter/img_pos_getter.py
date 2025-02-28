from ...llm import LLMAPIClient
import base64
import mss
import io
import logging
import os
import platform
import time
from typing import Optional
from PIL import Image
from pyvirtualdisplay import Display
from PIL import ImageDraw
import subprocess
from subprocess import TimeoutExpired

class ImagePosGetter:
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.client = LLMAPIClient(model=model, json_mode=True)
        if self.client.host == "anthropic":
            self.image_pos_getter = AnthropicImagePosGetter(model=model)
        elif self.client.host == "google":
            self.image_pos_getter = GeminiImagePosGetter(model=model)
            
    def take_screenshot(self):
        return self.image_pos_getter.take_screenshot()
    
    def get_img_pos(self, img_object_name: str):
        return self.image_pos_getter.get_img_pos(img_object_name)
    
    def get_img_bbox(self, img_object_name: str):
        if self.client.host == "anthropic":
            raise Exception("Anthropic does not support bbox")
        return self.image_pos_getter.get_img_bbox(img_object_name)
    
    def draw_point_on_screenshot(self, coordinate):
        self.image_pos_getter.draw_point_on_screenshot(coordinate)
        
    def draw_bbox_on_screenshot(self, bbox):
        if self.client.host == "anthropic":
            raise Exception("Anthropic does not support bbox")
        self.image_pos_getter.draw_bbox_on_screenshot(bbox)

class AnthropicImagePosGetter:
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.image_pos_utils = ImgGetterUtils(model=model)
        self.client = LLMAPIClient(model=model, json_mode=True)
        
    def take_screenshot(self):
        return self.image_pos_utils.take_screenshot()
        
    def get_img_pos(self, img_object_name: str):
        try:
            img_object_pos = self._get_image_pos_info(img_object_name)
            if not (img_object_pos["x"] and img_object_pos["y"]):
                raise Exception("x,yをキーとするJSONが返されませんでした")
        except Exception as e:
            logging.error(f"座標の取得に失敗しました: {e}")
            raise ValueError(f"座標の取得に失敗しました: {e}")
        return img_object_pos
    
    def _get_image_pos_info(self, img_object_name: str):
        screenshot_data = self.image_pos_utils.take_screenshot()
        if screenshot_data is None:
            logging.error("スクリーンショットの取得に失敗しました")
            raise Exception("スクリーンショットの取得に失敗しました")
        
        message = f"""Find the center coordinates of "{img_object_name}" in the provided image and return as dictionary:
ex) {{"response": {{"x": <pixel_x>, "y": <pixel_y>}}}}
Note: Do not take a new screenshot, use only the image I provided."""
        monitor_width, monitor_height = self.image_pos_utils._get_monitor_info()
        try:
            class Tool:
                pass
            tool = Tool()

            img_object_pos = self.client.request_messages(
                tools=[
                    {
                        "type": "computer_20241022",
                        "name": "computer",
                        "display_width_px": monitor_width,
                        "display_height_px": monitor_height,
                        "display_number": 1,
                    }
                ],
                tool_object=tool,
                messages=[
                    {
                        "role": "user", "content": [
                            {
                                "type": "text", 
                                "text": message
                            },
                            {
                                "type": "image", 
                                "image": {
                                    "type": "base64",
                                    "content": screenshot_data
                                }
                            }
                        ]
                    },
                ],
                betas=["computer-use-2024-10-22"],
            )
        except Exception as e:
            logging.error(f"座標の取得に失敗しました: {e}")
            raise ValueError(f"座標の取得に失敗しました: {e}")
        monitor_width, monitor_height = self.image_pos_utils._get_monitor_info()
        img_object_pos["response"]["monitor_width"] = monitor_width
        img_object_pos["response"]["monitor_height"] = monitor_height
        img_object_pos = img_object_pos["response"]
        return img_object_pos
        
    def draw_point_on_screenshot(self, coordinate):
        """スクリーンショットに赤い点を描画する"""
        try:
            # 最新のスクリーンショットを開く
            with Image.open('latest_screenshot.jpg') as img:
                # 画像編集用のDrawオブジェクトを作成
                draw = ImageDraw.Draw(img)
                
                # 赤い点を描画（半径5ピクセル）
                x, y = coordinate["x"], coordinate["y"]
                draw.ellipse([x-5, y-5, x+5, y+5], fill='red')
                
                # 更新された画像を保存
                img.save('latest_screenshot_with_point.jpg')
                
        except Exception as e:
            logging.error(f"点の描画に失敗しました: {e}")
            

class GeminiImagePosGetter:
    def __init__(self, model: str = "gemini-1.5-pro"):
        self.image_pos_utils = ImgGetterUtils(model=model)
        self.client = LLMAPIClient(model=model, json_mode=True)
        
    def take_screenshot(self):
        return self.image_pos_utils.take_screenshot()
        
    def get_img_pos(self, img_object_name: str):
        bbox_info = self.get_img_bbox(img_object_name)
        center_coordinate = self._get_bbox_center(bbox_info)
        center_coordinate["monitor_width"] = bbox_info["monitor_width"]
        center_coordinate["monitor_height"] = bbox_info["monitor_height"]
        try:
            if not (center_coordinate["x"] and center_coordinate["y"]):
                raise Exception("x,yをキーとするJSONが返されませんでした")
        except Exception as e:
            logging.error(f"座標の取得に失敗しました: {e}")
            raise ValueError(f"座標の取得に失敗しました: {e}")
        return center_coordinate
        
    def get_img_bbox(self, img_object_name: str):
        try:
            bbox_info = self._get_image_pos_info(img_object_name)
            if not (bbox_info["xmin"] and bbox_info["xmax"] and bbox_info["ymin"] and bbox_info["ymax"]):
                raise Exception("xmin,xmax,ymin,ymaxをキーとするJSONが返されませんでした")
        except Exception as e:
            logging.error(f"境界ボックスの取得に失敗しました: {e}")
            raise ValueError(f"境界ボックスの取得に失敗しました: {e}")
        return bbox_info
    
    def _get_image_pos_info(self, img_object_name: str):
        screenshot_data = self.image_pos_utils.take_screenshot()
        if screenshot_data is None:
            logging.error("スクリーンショットの取得に失敗しました")
            raise Exception("スクリーンショットの取得に失敗しました")
        
        message = f"""Return a bounding box for {img_object_name}. \n [ymin, xmin, ymax, xmax]"""
        try:
            response = self.client.request_messages(
                messages=[
                    {"role": "user", "content": message},
                    {"role": "user", "content": "Only return the JSON object, no other text or comments."}
                ],
                images=[{"base64": screenshot_data}],
            )
        except Exception as e:
            logging.error(f"境界ボックスの取得に失敗しました: {e}")
            raise ValueError(f"境界ボックスの取得に失敗しました: {e}")
        monitor_width, monitor_height = self.image_pos_utils._get_monitor_info()
        bbox = self._convert_bbox_coordinates(response, monitor_width, monitor_height)
        bbox["monitor_width"] = monitor_width
        bbox["monitor_height"] = monitor_height
        return bbox
    
    def draw_bbox_on_screenshot(self, bbox):
        """スクリーンショットに境界ボックスを描画"""
        try:
            with Image.open('latest_screenshot.jpg') as img:
                draw = ImageDraw.Draw(img)
                
                # 赤い矩形を描画（線の太さ2ピクセル）
                draw.rectangle([bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]], outline='red', width=2)
                
                img.save('latest_screenshot_with_bbox.jpg')
                
        except Exception as e:
            logging.error(f"境界ボックスの描画に失敗しました: {e}")

    def draw_point_on_screenshot(self, coordinate):
        """スクリーンショットに赤い点を描画する"""
        try:
            # 最新のスクリーンショットを開く
            with Image.open('latest_screenshot.jpg') as img:
                # 画像編集用のDrawオブジェクトを作成
                draw = ImageDraw.Draw(img)
                
                # 赤い点を描画（半径5ピクセル）
                x, y = coordinate["x"], coordinate["y"]
                draw.ellipse([x-5, y-5, x+5, y+5], fill='red')
                
                # 更新された画像を保存
                img.save('latest_screenshot_with_point.jpg')
                
        except Exception as e:
            logging.error(f"点の描画に失敗しました: {e}")
        
    def _convert_bbox_coordinates(self, bbox, img_width, img_height):
        """境界ボックスの座標を画像の実際のサイズに変換"""
        for i, value in enumerate(bbox):
            if i == 0:
                ymin = value
            elif i == 1:
                xmin = value
            elif i == 2:
                ymax = value
            elif i == 3:
                xmax = value
        return {
            "ymin": int(ymin * img_height) / 1000,  # ymin
            "xmin": int(xmin * img_width) / 1000,   # xmin
            "ymax": int(ymax * img_height) / 1000,  # ymax
            "xmax": int(xmax * img_width) / 1000    # xmax
        }
    
    def _get_bbox_center(self, bbox):
        """境界ボックスの中央座標を計算"""
        xmin, ymin, xmax, ymax = bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]
        center_x = (xmin + xmax) // 2
        center_y = (ymin + ymax) // 2
        bbox_center = {
            "x": center_x,
            "y": center_y
        }
        return bbox_center
        
class ImgGetterUtils:
    def __init__(self,
                 model: str = "claude-3-5-sonnet-20241022"):
        assert model in ["claude-3-5-sonnet-20241022", "gemini-1.5-pro"], "only claude-3-5-sonnet-20241022 and gemini-1.5-pro are supported"
        self.client = LLMAPIClient(model=model)
    
    def take_screenshot(self) -> Optional[str]:
        try:
            if platform.system() == 'Linux' and self._is_running_in_docker():
                logging.info("Linuxでスクリーンショットを取得します")
                
                # VNC用のDISPLAY設定を使用
                os.environ['DISPLAY'] = ':1'
                logging.info(f"DISPLAY設定: {os.environ.get('DISPLAY')}")
                
                temp_path = '/tmp/temp_screenshot.png'
                try:
                    # 直接scrotを実行（suは使用しない）
                    cmd = ['scrot', '-z', '-o', temp_path]
                    logging.info(f"実行するコマンド: {' '.join(cmd)}")
                    
                    # subprocessの実行方法を変更
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        env=os.environ.copy()
                    )
                    
                    try:
                        stdout, stderr = process.communicate(timeout=10)
                        if process.returncode != 0:
                            logging.error(f"scrotコマンドエラー: {stderr.decode()}")
                            logging.error(f"scrot出力: {stdout.decode()}")
                            return None
                            
                    except TimeoutExpired:
                        process.kill()
                        logging.error("スクリーンショットのタイムアウト")
                        logging.error(f"プロセス状態: {process.poll()}")
                        return None

                except TimeoutExpired:
                    logging.error("スクリーンショットのタイムアウト")
                    # プロセスが残っていないか確認
                    subprocess.run(['pkill', 'scrot'])
                    return None
                except Exception as e:
                    logging.error(f"scrot実行エラー: {e}")
                    return None

                if not os.path.exists(temp_path):
                    logging.error("スクリーンショットの取得に失敗しました")
                    return None
                
                try:
                    # PILで画像を開く
                    img = Image.open(temp_path)
                    
                    # 既存の画像サイズ調整処理を維持
                    max_dimension = 1920
                    ratio = min(max_dimension / img.width, max_dimension / img.height)
                    if ratio < 1:
                        new_width = int(img.width * ratio)
                        new_height = int(img.height * ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # 画像の保存と圧縮
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='JPEG', optimize=True, quality=85)
                    img.save('latest_screenshot.jpg', format='JPEG', optimize=True, quality=85)
                    
                    # 一時ファイルの削除
                    os.remove(temp_path)
                    
                    return base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                    
                except Exception as e:
                    logging.error(f"画像処理エラー: {e}")
                    return None
            else:
                logging.error("Linux環境ではないため、スクリーンショットを取得できません")
                return None
        except Exception as e:
            logging.error(f"スクリーンショット取得中にエラーが発生しました: {e}")
            return None
    
    def _is_running_in_docker(self):
        try:
            with open('/proc/1/cgroup', 'r') as f:
                return any('docker' in line for line in f)
        except FileNotFoundError:
            return False
        
    def _setup_virtual_display(self) -> Optional[Display]:
        """Linux環境で仮想ディスプレイをセットアップ"""
        if platform.system() == 'Linux':
            try:
                # Xvfbの詳細な設定を追加
                os.environ['XAUTHORITY'] = '/home/abc/.Xauthority'
                display = Display(visible=0, size=(1024, 768), backend='xvfb', 
                                color_depth=24, extra_args=['-screen', '0', '1024x768x24'])
                display.start()
                os.environ['DISPLAY'] = display.new_display_var
                # ディスプレイの初期化を待機
                time.sleep(5)
                return display
            except Exception as e:
                logging.error(f"仮想ディスプレイの設定に失敗: {e}")
                return None
        return None
    
    # モニター情報を動的に取得
    def _get_monitor_info(self):
        try:
            with mss.mss() as sct:
                # X11環境のプライマリモニターを取得
                if platform.system() == 'Linux' and self._is_running_in_docker():
                    # X11のディスプレイ情報を取得
                    display = os.environ.get('DISPLAY', ':0.0')
                    logging.info(f"X11 Display: {display}")
                    
                    # プライマリモニターの情報を取得
                    primary_monitor = sct.monitors[1]  # インデックス1がプライマリモニター
                    width = primary_monitor["width"]
                    height = primary_monitor["height"]
                    logging.info(f"検出されたディスプレイサイズ: {width}x{height}")
                    return width, height
                else:
                    primary_monitor = sct.monitors[1]
                    return primary_monitor["width"], primary_monitor["height"]
        except Exception as e:
            logging.error(f"モニター情報の取得に失敗: {e}")
            # デフォルト値を返す
            return 1024, 768
