import asyncio
from pymilvus import MilvusClient
from typing import List, Dict, Any, Optional

class MilvusManager:
    """
    Milvusベクターデータベースを管理するためのクラス。
    
    このクラスは、Milvusの基本的な操作（コレクションの作成、データの挿入、検索、
    クエリ、削除など）をカプセル化します。
    
    Attributes:
        client (MilvusClient): Milvusクライアントのインスタンス
    """

    def __init__(self, db_path: str = "milvus.db", lock: Optional[asyncio.Lock] = None):
        """
        MilvusManagerを初期化します。

        Args:
            db_path (str): Milvusデータベースファイルのパス。デフォルトは"milvus.db"
        """
        self.client = MilvusClient(db_path)
        self.lock = lock
        
    def create_collection(self, collection_name: str, dimension: int) -> None:
        """
        新しいコレクションを作成します。既存のコレクションが存在する場合はエラーを発生させます。

        Args:
            collection_name (str): 作成するコレクションの名前
            dimension (int): ベクトルの次元数

        Raises:
            ValueError: 既存のコレクションが存在する場合に発生

        Example:
            >>> manager = MilvusManager()
            >>> manager.create_collection("my_collection", 768)
        """
        if self.client.has_collection(collection_name):
            raise ValueError(f"コレクション '{collection_name}' は既に存在します。")
        
        self.client.create_collection(
            collection_name=collection_name,
            dimension=dimension
        )

    def insert_data(self, collection_name: str, data: List[Dict[str, Any]]) -> Dict:
        """
        コレクションにデータを挿入します。

        Args:
            collection_name (str): データを挿入するコレクションの名前
            data (List[Dict[str, Any]]): 挿入するデータのリスト。各データは辞書形式で、
                                       'id'、'vector'、その他のメタデータフィールドを含む

        Returns:
            Dict: 挿入結果を含む辞書（挿入件数、ID、処理時間など）

        Example:
            >>> data = [
            ...     {"id": 1, "vector": [0.1, 0.2, ...], "text": "sample text"},
            ...     {"id": 2, "vector": [0.3, 0.4, ...], "text": "another text"}
            ... ]
            >>> manager.insert_data("my_collection", data)
        """
        return self.client.insert(
            collection_name=collection_name,
            data=data
        )
    
    async def async_insert_data(self, collection_name: str, data: List[Dict[str, Any]]) -> Dict:
        async with self.lock:
            return self.insert_data(collection_name, data)

    def search_vectors(
        self,
        collection_name: str,
        query_vectors: List[List[float]],
        limit: int = 10,
        output_fields: Optional[List[str]] = None,
        filter: Optional[str] = None
    ) -> List:
        """
        ベクトル検索を実行します。

        Args:
            collection_name (str): 検索対象のコレクション名
            query_vectors (List[List[float]]): 検索クエリベクトルのリスト
            limit (int): 返す結果の最大数。デフォルトは10
            output_fields (Optional[List[str]]): 結果に含めるフィールド名のリスト
            filter (Optional[str]): 検索結果をフィルタリングする条件式

        Returns:
            List: 検索結果のリスト。各結果には類似度スコアと該当するエンティティ情報が含まれる

        Example:
            >>> query = [[0.1, 0.2, ...]]  # 検索クエリベクトル
            >>> results = manager.search_vectors(
            ...     "my_collection",
            ...     query,
            ...     limit=5,
            ...     output_fields=["text"],
            ...     filter="category == 'news'"
            ... )
        """
        return self.client.search(
            collection_name=collection_name,
            data=query_vectors,
            limit=limit,
            output_fields=output_fields,
            filter=filter
        )
    
    async def async_search_vectors(
        self,
        collection_name: str,
        query_vectors: List[List[float]],
        limit: int = 10,
        output_fields: Optional[List[str]] = None,
        filter: Optional[str] = None
    ) -> List:
        return self.search_vectors(collection_name, query_vectors, limit, output_fields, filter)

    def query_by_filter(
        self,
        collection_name: str,
        filter: str,
        output_fields: Optional[List[str]] = None
    ) -> List:
        """
        フィルター条件に基づいてデータをクエリします。

        Args:
            collection_name (str): クエリ対象のコレクション名
            filter (str): フィルター条件を表す式
            output_fields (Optional[List[str]]): 結果に含めるフィールド名のリスト

        Returns:
            List: クエリ結果のリスト

        Example:
            >>> results = manager.query_by_filter(
            ...     "my_collection",
            ...     "age >= 20 and category == 'news'",
            ...     ["id", "text"]
            ... )
        """
        return self.client.query(
            collection_name=collection_name,
            filter=filter,
            output_fields=output_fields
        )
    
    async def async_query_by_filter(
        self,
        collection_name: str,
        filter: str,
        output_fields: Optional[List[str]] = None
    ) -> List:
        return self.query_by_filter(collection_name, filter, output_fields)

    def query_by_ids(
        self,
        collection_name: str,
        ids: List[int],
        output_fields: Optional[List[str]] = None
    ) -> List:
        """
        指定されたIDのエンティティを取得します。

        Args:
            collection_name (str): クエリ対象のコレクション名
            ids (List[int]): 取得したいエンティティのIDリスト
            output_fields (Optional[List[str]]): 結果に含めるフィールド名のリスト

        Returns:
            List: クエリ結果のリスト

        Example:
            >>> results = manager.query_by_ids(
            ...     "my_collection",
            ...     [1, 2, 3],
            ...     ["text", "vector"]
            ... )
        """
        return self.client.query(
            collection_name=collection_name,
            ids=ids,
            output_fields=output_fields
        )
    
    async def async_query_by_ids(
        self,
        collection_name: str,
        ids: List[int],
        output_fields: Optional[List[str]] = None
    ) -> List:
        return self.query_by_ids(collection_name, ids, output_fields)

    def delete_by_ids(self, collection_name: str, ids: List[int]) -> List:
        """
        指定されたIDのエンティティを削除します。

        Args:
            collection_name (str): 削除対象のコレクション名
            ids (List[int]): 削除するエンティティのIDリスト

        Returns:
            List: 削除操作の結果

        Example:
            >>> manager.delete_by_ids("my_collection", [1, 2, 3])
        """
        return self.client.delete(
            collection_name=collection_name,
            ids=ids
        )

    def delete_by_filter(self, collection_name: str, filter: str) -> List:
        """
        フィルター条件に一致するエンティティを削除します。

        Args:
            collection_name (str): 削除対象のコレクション名
            filter (str): 削除条件を表す式

        Returns:
            List: 削除操作の結果

        Example:
            >>> manager.delete_by_filter(
            ...     "my_collection",
            ...     "age < 20 or category == 'old'"
            ... )
        """
        return self.client.delete(
            collection_name=collection_name,
            filter=filter
        )

    def drop_collection(self, collection_name: str) -> None:
        """
        コレクションを完全に削除します。

        Args:
            collection_name (str): 削除するコレクションの名前

        Example:
            >>> manager.drop_collection("my_collection")
        """
        self.client.drop_collection(collection_name=collection_name)

    def has_collection(self, collection_name: str) -> bool:
        """
        指定されたコレクションが存在するかどうかを確認します。

        Args:
            collection_name (str): 確認するコレクションの名前

        Returns:
            bool: コレクションが存在する場合はTrue、存在しない場合はFalse

        Example:
            >>> if manager.has_collection("my_collection"):
            ...     print("Collection exists!")
        """
        return self.client.has_collection(collection_name)