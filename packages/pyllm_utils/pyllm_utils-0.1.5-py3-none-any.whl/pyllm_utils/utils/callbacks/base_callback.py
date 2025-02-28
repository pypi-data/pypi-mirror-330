import logging
import os
import pathlib
import sys
from logging.handlers import RotatingFileHandler

class BaseCallback:
    def __init__(self, shell_log_level=logging.INFO):

        # ログディレクトリの作成
        log_dir = pathlib.Path(__file__).parent.parent.parent / "eve_logs"
        memory_log_dir = log_dir / "memory"
        log_dir.mkdir(parents=True, exist_ok=True)
        memory_log_dir.mkdir(parents=True, exist_ok=True)

        # 各ログファイルのパス設定
        self.log_files = {
            'all': log_dir / 'all.log',
            'brain': log_dir / 'brain.log',
            'action': log_dir / 'action.log',
            'memory_all': memory_log_dir / 'all.log',
            'memory_memorize': memory_log_dir / 'memorize.log',
            'memory_recall': memory_log_dir / 'recall.log',
            'error': log_dir / 'error.log'
        }

        # ロガーの設定
        self.loggers = {}
        
        # まずallロガーを設定
        all_logger = logging.getLogger('eve')
        all_logger.setLevel(logging.INFO)
        
        # allロガーのハンドラー設定
        all_file_handler = RotatingFileHandler(self.log_files['all'], maxBytes=10*1024*1024, backupCount=5)
        all_file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        all_file_handler.setFormatter(all_file_formatter)
        all_logger.addHandler(all_file_handler)
        
        # シェル出力用のハンドラーを追加
        shell_handler = logging.StreamHandler(sys.stdout)
        shell_formatter = logging.Formatter('%(message)s')
        shell_handler.setFormatter(shell_formatter)
        shell_handler.setLevel(shell_log_level)
        all_logger.addHandler(shell_handler)
        
        self.loggers['all'] = all_logger

        # 他のロガーを設定
        for name, path in self.log_files.items():
            if name == 'all':
                continue
            
            logger = logging.getLogger(f'eve.{name}')
            logger.setLevel(logging.INFO)
            logger.propagate = True  # 親ロガー（all）にも伝播
            
            file_handler = RotatingFileHandler(path, maxBytes=10*1024*1024, backupCount=5)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            self.loggers[name] = logger

        self._current_response = []  # ストリーミング応答を保存するためのバッファ

    def _log_to_all(self, level, message):
        """すべてのメッセージをallログに記録"""
        if level == 'error':
            self.loggers['all'].error(message)
            self.loggers['error'].error(message)
        else:
            self.loggers['all'].info(message)

    def base_callback(self, text):
        self._log_to_all('info', text)

    def chat_callback(self, chunk):
        if chunk is None:
            if self._current_response:
                complete_response = ''.join(self._current_response)
                self._log_to_all('info', f"Assistant: {complete_response}")
                self._current_response = []
        else:
            self._current_response.append(chunk)

    def brain_input_callback(self, brain_prompt):
        message = f"Brain Prompt: {brain_prompt}"
        self._log_to_all('info', message)
        self.loggers['brain'].info(message)

    def brain_output_callback(self, chat_result, thought_result, action_result, memory_result, read_result):
        for result_name, result in [
            ("Chat", chat_result),
            ("Thought", thought_result),
            ("Action", action_result),
            ("Memory", memory_result),
            ("Read", read_result)
        ]:
            message = f"{result_name} Result: {result}"
            self._log_to_all('info', message)
            self.loggers['brain'].info(message)

    def computer_use_output_callback(self, message):
        if text := message.get("text"):
            message = f"Assistant: {text}"
            self._log_to_all('info', message)
            self.loggers['action'].info(message)

    def computer_use_tool_output_callback(self, tool_output, tool_id):
        message = f"Tool Output ({tool_id}):"
        self._log_to_all('info', message)
        self.loggers['action'].info(message)
        if tool_output.output:
            message = tool_output.output
            self._log_to_all('info', message)
            self.loggers['action'].info(message)
        if tool_output.base64_image:
            message = "画像が撮影されました。"
            self._log_to_all('info', message)
            self.loggers['action'].info(message)
        if tool_output.error:
            message = f"Error: {tool_output.error}"
            self._log_to_all('error', message)
            self.loggers['error'].error(message)

    def computer_use_api_response_callback(self, request, response, error):
        message = "\nAPI Log:"
        self._log_to_all('info', message)
        self.loggers['action'].info(message)
        message = f"Request: {request.url}"
        self._log_to_all('info', message)
        self.loggers['action'].info(message)
        if response:
            message = f"Response: {response.status_code}"
            self._log_to_all('info', message)
            self.loggers['action'].info(message)
        if error:
            message = f"Error: {error}"
            self._log_to_all('error', message)
            self.loggers['error'].error(message)

    def normal_gui_controller_callback(self, plan, executed_action, remaining_actions):
        message = f"Plan: {plan}"
        self._log_to_all('info', message)
        self.loggers['action'].info(message)
        message = f"Executed Action: {executed_action}"
        self._log_to_all('info', message)
        self.loggers['action'].info(message)
        message = f"Remaining Actions: {remaining_actions}"
        self._log_to_all('info', message)
        self.loggers['action'].info(message)

    def memorized_sentence_callback(self, sentence):
        message = f"Memorized Sentence: {sentence}"
        self._log_to_all('info', message)
        self.loggers['memory_memorize'].info(message)

    def memorize_new_clause_relation_callback(self, word_info_1, word_info_2):
        message = f"Memorized New Clause Relation: {word_info_1} - {word_info_2}"
        self._log_to_all('info', message)
        self.loggers['memory_memorize'].info(message)

    def memorize_existing_clause_relation_callback(self, word_info_1, word_info_2):
        message = f"Memorized Existing Clause Relation: {word_info_1} - {word_info_2}"
        self._log_to_all('info', message)
        self.loggers['memory_memorize'].info(message)

    def memorize_new_independent_word_callback(self, independent_word):
        message = f"Memorized New Independent Word: {independent_word}"
        self._log_to_all('info', message)
        self.loggers['memory_memorize'].info(message)

    def memorize_new_clause_relation_callback(self, clause, independent_word):
        message = f"Memorized New Clause Relation: {clause} - {independent_word}"
        self._log_to_all('info', message)
        self.loggers['memory_memorize'].info(message)

    def choose_keywords_for_recall_callback(self, response):
        message = f"Choose Keywords for Recall: {response}"
        self._log_to_all('info', message)
        self.loggers['memory_recall'].info(message)

    def recalled_words_callback(self, recalled_words):
        message = f"Recalled Words: {recalled_words}"
        self._log_to_all('info', message)
        self.loggers['memory_recall'].info(message)

    def error_callback(self, error):
        message = f"Error: {error}"
        self._log_to_all('error', message)
        self.loggers['error'].error(message)