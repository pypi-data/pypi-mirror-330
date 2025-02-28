from redis import Redis
from typing import Any, Optional, List, Dict, Union
import json

class RedisManager:
    """
    Redisデータベースを管理するためのクラス。
    
    このクラスは、Redisの基本的な操作（データの設定、取得、削除、
    有効期限の設定など）をカプセル化します。
    
    Attributes:
        client (Redis): Redisクライアントのインスタンス
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None
    ):
        """
        RedisManagerを初期化します。

        Args:
            host (str): Redisサーバーのホスト名。デフォルトは"localhost"
            port (int): Redisサーバーのポート番号。デフォルトは6379
            db (int): 使用するデータベース番号。デフォルトは0
            password (Optional[str]): Redisサーバーのパスワード
        """
        self.client = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )

    def set_value(
        self,
        key: str,
        value: Any,
        expire_seconds: Optional[int] = None
    ) -> bool:
        """
        キーと値のペアを保存します。

        Args:
            key (str): 保存するキー
            value (Any): 保存する値（自動的にJSON形式にシリアライズされます）
            expire_seconds (Optional[int]): キーの有効期限（秒）

        Returns:
            bool: 保存が成功した場合はTrue

        Example:
            >>> manager = RedisManager()
            >>> manager.set_value("user:1", {"name": "田中", "age": 30}, 3600)
        """
        serialized_value = json.dumps(value, ensure_ascii=False)
        return self.client.set(key, serialized_value, ex=expire_seconds)

    def get_value(self, key: str, default: Any = None) -> Any:
        """
        指定されたキーの値を取得します。

        Args:
            key (str): 取得するキー
            default (Any): キーが存在しない場合のデフォルト値

        Returns:
            Any: 保存された値（JSONからデシリアライズされた形式）

        Example:
            >>> value = manager.get_value("user:1")
            >>> print(value)  # {"name": "田中", "age": 30}
        """
        value = self.client.get(key)
        if value is None:
            return default
        return json.loads(value)

    def delete_keys(self, *keys: str) -> int:
        """
        指定されたキーを削除します。

        Args:
            *keys (str): 削除するキー（複数指定可能）

        Returns:
            int: 削除されたキーの数

        Example:
            >>> manager.delete_keys("user:1", "user:2")
        """
        return self.client.delete(*keys)

    def exists(self, *keys: str) -> int:
        """
        指定されたキーが存在するかどうかを確認します。

        Args:
            *keys (str): 確認するキー（複数指定可能）

        Returns:
            int: 存在するキーの数

        Example:
            >>> if manager.exists("user:1"):
            ...     print("キーが存在します")
        """
        return self.client.exists(*keys)

    def expire(self, key: str, seconds: int) -> bool:
        """
        キーの有効期限を設定します。

        Args:
            key (str): 対象のキー
            seconds (int): 有効期限（秒）

        Returns:
            bool: 設定が成功した場合はTrue

        Example:
            >>> manager.expire("user:1", 3600)  # 1時間後に期限切れ
        """
        return self.client.expire(key, seconds)

    def ttl(self, key: str) -> int:
        """
        キーの残り有効期限を取得します。

        Args:
            key (str): 対象のキー

        Returns:
            int: 残り時間（秒）。キーが存在しない場合は-2、
                 有効期限が設定されていない場合は-1

        Example:
            >>> remaining = manager.ttl("user:1")
            >>> print(f"残り{remaining}秒")
        """
        return self.client.ttl(key)

    def scan_keys(self, pattern: str = "*") -> List[str]:
        """
        パターンに一致するすべてのキーを取得します。

        Args:
            pattern (str): 検索パターン。デフォルトは"*"（すべてのキー）

        Returns:
            List[str]: マッチしたキーのリスト

        Example:
            >>> user_keys = manager.scan_keys("user:*")
        """
        return [key for key in self.client.scan_iter(pattern)]

    def increment(self, key: str, amount: int = 1) -> int:
        """
        キーの値を指定された量だけ増加させます。

        Args:
            key (str): 対象のキー
            amount (int): 増加量。デフォルトは1

        Returns:
            int: 増加後の値

        Example:
            >>> manager.increment("visits", 1)
        """
        return self.client.incrby(key, amount)

    def set_hash(self, key: str, mapping: Dict[str, Any]) -> bool:
        """
        ハッシュフィールドを設定します。

        Args:
            key (str): ハッシュのキー
            mapping (Dict[str, Any]): フィールドと値のマッピング

        Returns:
            bool: 設定が成功した場合はTrue

        Example:
            >>> manager.set_hash("user:1:details", {
            ...     "name": "田中",
            ...     "email": "tanaka@example.com"
            ... })
        """
        serialized_mapping = {
            k: json.dumps(v, ensure_ascii=False)
            for k, v in mapping.items()
        }
        return self.client.hset(key, mapping=serialized_mapping)

    def get_hash(self, key: str) -> Dict[str, Any]:
        """
        ハッシュの全フィールドと値を取得します。

        Args:
            key (str): ハッシュのキー

        Returns:
            Dict[str, Any]: フィールドと値のマッピング

        Example:
            >>> details = manager.get_hash("user:1:details")
        """
        result = self.client.hgetall(key)
        return {
            k: json.loads(v)
            for k, v in result.items()
        }

if __name__ == "__main__":
    manager = RedisManager()
    