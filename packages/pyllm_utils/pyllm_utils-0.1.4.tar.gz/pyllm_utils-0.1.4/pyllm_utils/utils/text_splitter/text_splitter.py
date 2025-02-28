import logging
from ...openai_api.openai_client import OpenAIClient
from sklearn.metrics.pairwise import cosine_similarity
import tiktoken
import re
from typing import List, Optional
import time

class TextSplitter:
    def __init__(
        self,
        min_chunk_tokens: int = 100,
        max_chunk_tokens: int = 500,
        similarity_threshold: float = 0.7,
        agent_model: str = "gpt-4o-mini",
        model: str = "gpt-4o-mini",
        min_sentences_per_chunk: int = 3,
        split_method: str = "similarity"
    ):
        """
        Parameters:
            min_chunk_tokens (int): チャンクの最小トークン数
            max_chunk_tokens (int): チャンクの最大トークン数
            similarity_threshold (float): チャンクを結合する類似度の閾値
            model (str): 使用するモデル名（トークナイザーの選択に使用）
            min_sentences_per_chunk (int): チャンク分割時の最小文章数
            split_method (str): 分割方法 ("similarity" または "agent")
        """
        self.min_chunk_tokens = min_chunk_tokens
        self.max_chunk_tokens = max_chunk_tokens
        self.similarity_threshold = similarity_threshold
        self.min_sentences_per_chunk = min_sentences_per_chunk
        
        # tiktokenエンコーダーの初期化
        self.encoding = tiktoken.encoding_for_model(model)
        
        # 分割パターンを保存する際に、キャプチャグループを使用
        self.paragraph_separator = r'(\n\s*\n)'
        self.secondary_separators = [
            '\n',
            '。', '！', '？',  # 全角
            '.', '!', '?',    # 半角
        ]

        self.split_method = split_method
        self.agent = OpenAIClient(model=agent_model)

    def _count_tokens(self, text: str) -> int:
        """テキストのトークン数を計算"""
        return len(self.encoding.encode(text))

    def _get_similarity(self, text1: str, text2: str) -> float:
        """2つのテキスト間の類似度を計算"""
        if not text1 or not text2:
            return 0.0
        
        # 埋め込み取得の最大試行回数
        max_retries = 3
        # リトライ間の待機時間（秒）
        retry_delay = 1
        
        # text1の埋め込み取得
        for attempt in range(max_retries):
            try:
                emb1 = self.agent.request_embeddings(input=text1, model="text-embedding-3-large")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    logging.error(f"text1の埋め込み取得に{max_retries}回失敗しました: {str(e)}")
                    raise Exception(f"text1の埋め込み取得に{max_retries}回失敗しました: {str(e)}")
                time.sleep(retry_delay * (attempt + 1))  # 待機時間を徐々に増やす
        
        # text2の埋め込み取得
        for attempt in range(max_retries):
            try:
                emb2 = self.agent.request_embeddings(input=text2, model="text-embedding-3-large")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    logging.error(f"text2の埋め込み取得に{max_retries}回失敗しました: {str(e)}")
                    raise Exception(f"text2の埋め込み取得に{max_retries}回失敗しました: {str(e)}")
                time.sleep(retry_delay * (attempt + 1))  # 待機時間を徐々に増やす
        
        return cosine_similarity([emb1], [emb2])[0][0]

    def _merge_small_chunks(self, chunks: List[dict]) -> List[dict]:
        """最小トークン数以下のチャンクを前後のチャンクと結合"""
        if len(chunks) <= 1:
            return chunks

        result = []
        i = 0
        while i < len(chunks):
            current_chunk = chunks[i]
            current_tokens = current_chunk['tokens']
            
            if current_tokens >= self.min_chunk_tokens:
                result.append(current_chunk)
                i += 1
                continue
            
            # 前後のチャンクとの類似度を計算
            prev_similarity = (self._get_similarity(chunks[i-1]['text'], current_chunk['text']) 
                             if i > 0 else 0.0)
            next_similarity = (self._get_similarity(current_chunk['text'], chunks[i+1]['text']) 
                             if i < len(chunks)-1 else 0.0)
            
            # 結合後のトークン数をチェック
            if prev_similarity > next_similarity and result:
                combined_text = result[-1]['text'] + current_chunk['text']
                result[-1] = {
                    'text': combined_text,
                    'tokens': result[-1]['tokens'] + current_chunk['tokens']
                }
            elif i < len(chunks)-1:
                combined_text = current_chunk['text'] + chunks[i+1]['text']
                chunks[i+1] = {
                    'text': combined_text,
                    'tokens': current_chunk['tokens'] + chunks[i+1]['tokens']
                }
            else:
                result.append(current_chunk)
            i += 1
            
        return result

    def _should_merge_chunks(self, chunk1: dict, chunk2: dict) -> bool:
        """チャンクを結合すべきかどうかを判断"""
        if self.split_method == "similarity":
            return self._get_similarity(chunk1['text'], chunk2['text']) >= self.similarity_threshold
        else:  # agent
            messages = [
                {"role": "system", "content": """
                あなたはテキスト分割の専門家です。
                2つのテキストチャンクを結合すべきかどうかを判断してください。
                判断基準：
                - トピックの一貫性
                - 文脈の連続性
                - 意味的なつながり
                回答は "should_merge" keyに true または false を指定したJSONを返してください。
                """},
                {"role": "user", "content": f"チャンク1:\n{chunk1['text']}\n\nチャンク2:\n{chunk2['text']}"}
            ]
            response = self.agent.request_messages(messages = messages, json_mode=True)
            return response["should_merge"]

    def _split_large_chunk(self, chunk: dict) -> List[dict]:
        """最大トークン数以上のチャンクを再分割"""
        if chunk['tokens'] <= self.max_chunk_tokens:
            return [chunk]
            
        # すべてのセパレータで一度に分割（セパレータは直前の文章に含める）
        current_text = chunk['text']
        all_splits = [current_text]
        
        for separator in self.secondary_separators:
            new_splits = []
            for text in all_splits:
                parts = text.split(separator)
                parts = [parts[i] + separator for i in range(len(parts)-1)] + [parts[-1]]
                current_chunk = ""
                
                for i, part in enumerate(parts):
                    if not part:
                        continue
                        
                    # セパレータのみで構成される部分は直前のチャンクに追加
                    if all(c in self.secondary_separators for c in part):
                        if current_chunk:
                            current_chunk += part
                        continue
                    
                    # 通常の部分の処理
                    if current_chunk:
                        new_splits.append(current_chunk)
                    current_chunk = part
                
                if current_chunk:
                    new_splits.append(current_chunk)
                    
            all_splits = new_splits
        
        def split_sentence_by_tokens(sentence: str, tokens: List[int]) -> List[dict]:
            """1文をトークン数で分割する"""
            splits = []
            for i in range(0, len(tokens), self.max_chunk_tokens):
                chunk_tokens = tokens[i:i + self.max_chunk_tokens]
                text = self.encoding.decode(chunk_tokens)
                splits.append({
                    'text': text,
                    'tokens': len(chunk_tokens)
                })
            return splits

        # 分割されたテキストとそのトークン数を事前に計算
        all_splits_with_tokens = []
        for text in all_splits:
            tokens = self.encoding.encode(text)
            all_splits_with_tokens.append({
                'text': text,
                'tokens': tokens,  # 生のトークンリストを保存
                'token_count': len(tokens)
            })

        # 分割されたテキストを適切なサイズで結合
        pre_merged_splits = []
        i = 0
        while i < len(all_splits_with_tokens):
            # 最大sentences_per_chunkから開始して、トークン数が超過する場合は減らしていく
            current_sentences = self.min_sentences_per_chunk
            while current_sentences > 0:
                batch = all_splits_with_tokens[i:i + current_sentences]
                total_tokens = sum(item['token_count'] for item in batch)
                
                if total_tokens <= self.max_chunk_tokens:
                    combined_text = ''.join(item['text'] for item in batch)
                    pre_merged_splits.append({
                        'text': combined_text,
                        'tokens': total_tokens
                    })
                    break
                current_sentences -= 1
            
            if current_sentences == 0:
                # 1文でも最大トークン数を超える場合は、トークンベースで分割
                sentence_data = all_splits_with_tokens[i]
                sub_splits = split_sentence_by_tokens(sentence_data['text'], sentence_data['tokens'])
                pre_merged_splits.extend(sub_splits)
                current_sentences = 1
                
            i += current_sentences

        # チャンクの結合処理（トークン数が既に計算済み）
        merged_chunks = []
        current_merged = pre_merged_splits[0]
        
        for i in range(1, len(pre_merged_splits)):
            next_chunk = pre_merged_splits[i]
            combined_tokens = current_merged['tokens'] + next_chunk['tokens']
            
            if combined_tokens <= self.max_chunk_tokens: 
                if combined_tokens < self.min_chunk_tokens:
                    current_merged = {
                        'text': current_merged['text'] + next_chunk['text'],
                    'tokens': combined_tokens
                    }
                elif self._should_merge_chunks(current_merged, next_chunk):
                    current_merged = {
                        'text': current_merged['text'] + next_chunk['text'],
                        'tokens': combined_tokens
                    }
                else:
                    merged_chunks.append(current_merged)
                    current_merged = next_chunk
            else:
                merged_chunks.append(current_merged)
                current_merged = next_chunk
        merged_chunks.append(current_merged)
        return merged_chunks

    def split_text(self, text: str) -> List[dict]:
        """テキストを分割する主要メソッド"""
        # 1. 段落で分割し、セパレータを保持
        parts = re.split(self.paragraph_separator, text)
        # キャプチャグループを使用した場合、分割されたテキストとセパレータが交互に出現するため、
        # 特別な処理は不要
        parts = [p for p in parts if p]
        initial_chunks = []
        for i in range(0, len(parts), 2):
            chunk_text = parts[i]
            if i + 1 < len(parts):
                chunk_text += parts[i + 1]  # セパレータを追加
            if chunk_text.strip():
                initial_chunks.append({
                    'text': chunk_text,
                    'tokens': self._count_tokens(chunk_text)
                })
        
        # 2. 小さいチャンクを結合
        merged_chunks = self._merge_small_chunks(initial_chunks)
        
        # 3. 大きいチャンクを再分割
        final_chunks = []
        for chunk in merged_chunks:
            if chunk['tokens'] > self.max_chunk_tokens:
                final_chunks.extend(self._split_large_chunk(chunk))
            else:
                final_chunks.append(chunk)
        
        return final_chunks

