import base64
from io import BytesIO
from PIL import Image
import tempfile
import requests # type: ignore
import logging
from typing import Optional
import os
import platform
import PIL # type: ignore
class DataEncoder:
    """
    データを様々な形式に変換するクラスです。
    """
    def __init__(self):
        pass
    
    def encode_audio_path_to_base64(self, audio_path: str) -> Optional[str]:
        """ローカルの音声ファイルをBase64エンコードされた文字列に変換します。

        Args:
            audio_path: 音声ファイルのパス

        Returns:
            Base64エンコードされた音声データ
            エラー時はNone
        """
        try:
            with open(audio_path, "rb") as audio_file:
                base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')
                return base64_audio
        except Exception as e:
            logging.error(f"音声のエンコード中にエラーが発生しました: {str(e)}")
            return None
        
    def encode_audio_url_to_base64(self, audio_url: str) -> Optional[str]:
        """URLから音声をダウンロードしBase64エンコードされた文字列に変換します。

        Args:
            audio_url: 音声のURL

        Returns:
            Base64エンコードされた音声データ
            エラー時はNone
        """
        try:
            response = requests.get(audio_url)
            response.raise_for_status()
            base64_audio = base64.b64encode(response.content).decode('utf-8')
            return base64_audio
        except Exception as e:
            logging.error(f"音声のダウンロード/エンコード中にエラーが発生しました: {str(e)}")
            return None
        
    def encode_audio_base64_to_base64str(self, base64_string: str) -> Optional[str]:
        """Base64文字列を OpenAI API 形式に変換します。

        Args:
            base64_string: Base64エンコードされた音声データ

        Returns:
            Base64エンコードされた音声データ
            エラー時はNone
        """
        try:
            return base64_string
        except Exception as e:
            logging.error(f"Base64データの変換中にエラーが発生しました: {str(e)}")
            return None

    def encode_image_path_to_base64str(self, image_path: str) -> Optional[str]:
        """ローカルの画像ファイルをBase64エンコードされた文字列に変換します。

        Args:
            image_path: 画像ファイルのパス

        Returns:
            Base64エンコードされた画像データ（data:image/[ext];base64,形式）
            エラー時はNone
        """
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                mime_type = self.get_image_mime_type(image_path)
                return f"data:{mime_type};base64,{base64_image}"
        except Exception as e:
            logging.error(f"画像のエンコード中にエラーが発生しました: {str(e)}")
            return None
        
    def encode_image_path_to_normal_base64str_and_media_type(self, image_path: str) -> Optional[str]:
        """ローカルの画像ファイルをBase64エンコードされたバイナリデータに変換します。
        """
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                media_type = self.get_image_mime_type(image_path)
                return base64_image, media_type
        except Exception as e:
            logging.error(f"画像のエンコード中にエラーが発生しました: {str(e)}")
            return None

    def encode_image_url_to_base64str(self, image_url: str) -> Optional[str]:
        """URLから画像をダウンロードしBase64エンコードされた文字列に変換します。

        Args:
            image_url: 画像のURL

        Returns:
            Base64エンコードされた画像データ（data:image/[ext];base64,形式）
            エラー時はNone
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            base64_image = base64.b64encode(response.content).decode('utf-8')
            mime_type = response.headers.get('content-type', 'image/jpeg')
            return f"data:{mime_type};base64,{base64_image}"
        except Exception as e:
            logging.error(f"画像のダウンロード/エンコード中にエラーが発生しました: {str(e)}")
            return None

    def encode_image_url_to_normal_base64str_and_media_type(self, image_url: str) -> Optional[str]:
        """URLから画像をダウンロードしBase64エンコードされたバイナリデータに変換します。
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            base64_image = base64.b64encode(response.content).decode('utf-8')
            media_type = response.headers.get('content-type', 'image/jpeg')
            return base64_image, media_type
        except Exception as e:
            logging.error(f"画像のダウンロード/エンコード中にエラーが発生しました: {str(e)}")
            return None

    def encode_image_base64_to_base64str(self, base64_string: str) -> Optional[str]:
        """Base64文字列を OpenAI API 形式に変換します。

        Args:
            base64_string: Base64エンコードされた画像データ

        Returns:
            Base64エンコードされた画像データ（data:image/[ext];base64,形式）
            エラー時はNone
        """
        try:
            # すでにdata:image形式の場合はそのまま返す
            if base64_string.startswith('data:image'):
                return base64_string
            
            # 画像形式を判定
            image_data = base64.b64decode(base64_string)
            with Image.open(BytesIO(image_data)) as img:
                mime_type = f"image/{img.format.lower()}"
                return f"data:{mime_type};base64,{base64_string}"
        except Exception as e:
            logging.error(f"Base64データの変換中にエラーが発生しました: {str(e)}")
            return None
        
    def encode_image_base64_to_normal_base64str_and_media_type(self, base64_string: str) -> Optional[str]:
        """Base64文字列をバイナリデータに変換します。
        """
        try:
            # Base64データから画像形式を判定
            image_data = base64.b64decode(base64_string)
            with Image.open(BytesIO(image_data)) as img:
                media_type = f"image/{img.format.lower()}"
            return base64_string, media_type
        except Exception as e:
            logging.error(f"Base64データの変換中にエラーが発生しました: {str(e)}")
            return None
        
    def encode_image_path_to_PIL(self, image_path: str) -> Optional[Image.Image]:
        """ローカルの画像ファイルを PIL 形式に変換します。
        
        Args:
            image_path: 画像ファイルのパス
            
        Returns:
            PIL Image オブジェクト（filename属性付き）
            エラー時はNone
        """
        try:
            with PIL.Image.open(image_path) as image:
                image.load()
                image_copy = image.copy()
                return image_copy
        except Exception as e:
            logging.error(f"画像のロード中にエラーが発生しました: {str(e)}")
            return None
        
    def encode_image_url_to_PIL(self, image_url: str) -> Optional[Image.Image]:
        """URLから画像をダウンロードし PIL 形式に変換します。
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            with PIL.Image.open(BytesIO(response.content)) as image:
                image.load()
                image_copy = image.copy()
                return image_copy
        except Exception as e:
            logging.error(f"画像のダウンロード/ロード中にエラーが発生しました: {str(e)}")
            return None
        
    def encode_image_base64_to_PIL(self, base64_string: str) -> Optional[Image.Image]:
        """Base64文字列を PIL 形式に変換します。
        """
        try:
            with PIL.Image.open(BytesIO(base64.b64decode(base64_string))) as image:
                image.load()
                image_copy = image.copy()
                return image_copy
        except Exception as e:
            logging.error(f"Base64データのロード中にエラーが発生しました: {str(e)}")
            return None
    
    def play_audio(self, base64_string: str) -> None:
        """Base64エンコードされた音声データを再生します。
        
        Args:
            base64_string: Base64エンコードされた音声データ
        """
        temp_file_path = None
        try:
            audio_data = base64.b64decode(base64_string)
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(audio_data)
                temp_file.flush()
                os.fsync(temp_file.fileno())

            if platform.system() == 'Linux':
                # ALSAの状態を確認
                alsa_check = os.system('aplay -l > /dev/null 2>&1')
                if alsa_check != 0:
                    logging.warning("ALSAサウンドデバイスが見つかりません。他のプレーヤーを試行します。")
                    
                players = [
                    ('aplay', 'aplay "{}"'),
                    ('paplay', 'paplay "{}"'),
                    ('mpg123', 'mpg123 "{}"'),
                    ('ffplay', 'ffplay -nodisp -autoexit "{}" > /dev/null 2>&1'),
                    ('mplayer', 'mplayer "{}" > /dev/null 2>&1')
                ]
                
                played = False
                for player_name, player_cmd in players:
                    if os.system(f'which {player_name} > /dev/null 2>&1') == 0:
                        cmd = player_cmd.format(temp_file_path)
                        result = os.system(cmd)
                        if result == 0:
                            logging.info(f"音声を{player_name}で再生しました")
                            played = True
                            break
                        else:
                            logging.debug(f"{player_name}での再生に失敗しました（終了コード: {result}）")
                
                if not played:
                    raise Exception("利用可能な音声プレーヤーが見つからないか、すべての再生試行が失敗しました")
                    
            elif platform.system() == 'Darwin':
                if os.system(f'afplay "{temp_file_path}"') == 0:
                    logging.info("音声をmacOSで再生しました")
                else:
                    raise Exception("macOSでの音声再生に失敗しました")
                    
            elif platform.system() == 'Windows':
                if os.system(f'start "" "{temp_file_path}"') == 0:
                    logging.info("音声をWindowsで再生しました")
                else:
                    raise Exception("Windowsでの音声再生に失敗しました")

        except Exception as e:
            logging.error(f"音声の再生中にエラーが発生しました: {str(e)}")
            raise

        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    logging.error(f"一時ファイルの削除中にエラーが発生しました: {str(e)}")
    
    def get_image_mime_type(self, file_path: str) -> str:
        """ファイルパスから MIME タイプを取得します。"""
        with Image.open(file_path) as img:
            return f"image/{img.format.lower()}"
        
    def get_audio_mime_type(self, file_path: str) -> str:
        """ファイルパスから MIME タイプを取得します。"""
        return f"audio/{file_path.split('.')[-1]}"
