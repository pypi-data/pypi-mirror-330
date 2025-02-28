import json
import re
from typing import Generator
import sys
import logging
class JsonStreamConverter:
    def _create_key_patterns(self, keys: list[str]) -> dict:
        return {key: re.compile(rf'"{key}"\s*:\s*') for key in keys}

    def _detect_json_start(self, token: str, in_json: bool) -> bool:
        return in_json or '{' in token

    def _detect_key_and_value(self, buffer: list[str], key_patterns: dict) -> tuple[str | None, str | None, list[dict]]:
        json_fragment = ''.join(buffer)
        keys_and_matches: list[dict] = []
        for key, pattern in key_patterns.items():
            match = pattern.search(json_fragment)
            if match:
                key_and_match = {
                    "key": key,
                    "match": {
                        "key_start": match.start(),
                        "key_end": match.end()
                    }
                }
                keys_and_matches.append(key_and_match)
        keys_and_values: list[dict] = []
        keys_and_matches.reverse()
        for i, key_and_match in enumerate(keys_and_matches):
            key_and_value = {}
            if i == 0:
                value = json_fragment[keys_and_matches[i]["match"]["key_end"]:]
                next_key_match_start = self._detect_key_match(value)
                if next_key_match_start:
                    key_and_value["key"] = key_and_match["key"]
                    key_and_value["value"] = value[:next_key_match_start]
                else:
                    key_and_value["key"] = key_and_match["key"]
                    key_and_value["value"] = value
            else:
                value = json_fragment[keys_and_matches[i]["match"]["key_end"]:keys_and_matches[i-1]["match"]["key_start"]]
                next_key_match_start = self._detect_key_match(value)
                if next_key_match_start:
                    key_and_value["key"] = key_and_match["key"]
                    key_and_value["value"] = value[:next_key_match_start]
                else:
                    key_and_value["key"] = key_and_match["key"]
                    key_and_value["value"] = value
            keys_and_values.insert(0, key_and_value)
        current_key = ""
        current_value = ""
        if keys_and_values:
            current_key = keys_and_values[-1]["key"]
            current_value = keys_and_values[-1]["value"]
        return current_key, current_value, keys_and_values
    
    def _detect_key_match(self, value: str):
        pattern = re.compile(r'"[^"\\]+"\s*:\s*')
        match = pattern.search(value)
        if match:
            return match.start()
        return None

    def _determine_value_type(self, token: str) -> str | None:
        stripped_token = token.strip()
        if stripped_token.startswith('"'):
            return 'string'
        elif re.match(r'^-?\d+(\.\d+)?([eE][+-]?\d+)?', stripped_token):
            return 'number'
        elif stripped_token.startswith('{'):
            return 'object'
        elif stripped_token.startswith('['):
            return 'array'
        elif stripped_token in ('true', 'false'):
            return 'boolean'
        elif stripped_token == 'null':
            return 'null'
        return None

    def _handle_value_end(self, value_type: str, value_buffer: list[str]) -> bool:
        on_going_value = "".join(value_buffer).strip()
        
        if value_type == 'string':
            if re.match(r'^"(?:[^"]|(?:\\"))*"', on_going_value):
                return True
        
        elif value_type == 'number':
            # 数値の終了条件を修正
            if re.match(r'(-?\d+(\.\d+)?([eE][+-]?\d+)?)?\s*(?:,|\n?\s*\})\s*', on_going_value):
                return True
        
        elif value_type == 'object':
            # オブジェクトの終了条件を修正
            start_brace_count, end_brace_count = 0, 0
            start_brace_count += on_going_value.count('{')
            end_brace_count += on_going_value.count('}')
            brace_count = start_brace_count - end_brace_count
            if brace_count == 0:
                return True
        
        elif value_type == 'array':
            # 配列の終了条件を修正
            start_bracket_count, end_bracket_count = 0, 0
            start_bracket_count += on_going_value.count('[')
            end_bracket_count += on_going_value.count(']')
            bracked_count = start_bracket_count - end_bracket_count
            if bracked_count == 0:
                return True
        
        elif value_type == 'boolean':
            # ブール値の終了条件を修正
            if on_going_value in ('true', 'false'):
                return True
        
        elif value_type == 'null':
            # nullの終了条件を修正
            if on_going_value == 'null':
                return True
        
        return False

    def _process_value(self, current_key: str, value_type: str, value_buffer: list[str], first_value_token: bool, last_value_token: bool) -> tuple[str, str]:
        if value_type == "string":
            if first_value_token:
                value_token = value_buffer[0].strip('"')
                if last_value_token:
                    value_token = re.sub(r'"[\s\S]*$', '', value_token)
                return current_key, value_token
            elif last_value_token:
                value_token = re.sub(r'"[\s\S]*$', '', value_buffer[-1])
                return current_key, value_token
            else:
                value_token = value_buffer[-1]
                return current_key, value_token
        elif value_type == "number":
            if first_value_token:
                value_token = value_buffer[0].strip()
                if last_value_token:
                    value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_token)
                return current_key, value_token
            elif last_value_token:
                value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_buffer[-1])
                return current_key, value_token
            else:
                value_token = value_buffer[-1]
                return current_key, value_token
        elif value_type == "object":
            if first_value_token:
                value_token = value_buffer[0].strip()
                if last_value_token:
                    value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_token)
                return current_key, value_token
            elif last_value_token:
                value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_buffer[-1])
                return current_key, value_token
            else:
                value_token = value_buffer[-1]
                return current_key, value_token
        elif value_type == "array":
            if first_value_token:
                value_token = value_buffer[0].strip()
                if last_value_token:
                    value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_token)
                return current_key, value_token
            elif last_value_token:
                value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_buffer[-1])
                return current_key, value_token
            else:
                value_token = value_buffer[-1]
                return current_key, value_token
        elif value_type == "boolean":
            if first_value_token:
                value_token = value_buffer[0].strip()
                if last_value_token:
                    value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_token)
                return current_key, value_token
            elif last_value_token:
                value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_buffer[-1])
                return current_key, value_token
            else:
                value_token = value_buffer[-1]
                return current_key, value_token
        elif value_type == "null":
            if first_value_token:
                value_token = value_buffer[0].strip()
                if last_value_token:
                    value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_token)
                return current_key, value_token
            elif last_value_token:
                value_token = re.sub(r'\s*(?:,|\n?\s*\})[\s\S]*$', '', value_buffer[-1])
                return current_key, value_token
            else:
                value_token = value_buffer[-1]
                return current_key, value_token
        return "", ""
                
    def stream_json_values(self, tokens: Generator[str, None, None], keys: list[str]) -> Generator[tuple[str, str], None, None]:
        buffer: list[str] = []
        in_json: bool = False
        current_key: str | None = None
        previous_key: str | None = None
        value_buffer: list[str] = []
        value_type: str | None = None
        first_value_token: bool = True
        last_value_token: bool = False

        key_patterns = self._create_key_patterns(keys)
        
        def reset_state():
            nonlocal current_key, value_type, in_json, buffer
            value_buffer.clear()
            current_key = None
            current_value = ""
            value_type = None
            on_going_json = "".join(buffer).strip()
            start_brace_count = on_going_json.count('{')
            end_brace_count = on_going_json.count('}')
            in_json = start_brace_count > end_brace_count

        def stream_json_values_generator():
            nonlocal current_key, previous_key, in_json, buffer, value_buffer, value_type, first_value_token, last_value_token
            for token in tokens:
                current_value = token
                previous_key = current_key
                in_json = self._detect_json_start(token, in_json)
                if in_json:
                    buffer.append(token)
                
                if not current_key and in_json:
                    current_key, current_value, keys_and_values = self._detect_key_and_value(buffer, key_patterns)
                    if len(keys_and_values) > 1:
                        for key_and_value in keys_and_values:
                            key = key_and_value["key"]
                            value = key_and_value["value"]
                            value_type = self._determine_value_type(value)
                            first_value_token = True
                            last_value_token = self._handle_value_end(value_type, [value])
                            yield self._process_value(key, value_type, [value], first_value_token, last_value_token)
                    if current_key and previous_key != current_key:
                        value_buffer.clear()
                        
                if (not value_type) and current_value.strip() and in_json:
                    value_type = self._determine_value_type(current_value)
                    first_value_token = True
                if value_type and in_json:
                    value_buffer.append(current_value)
                    last_value_token = self._handle_value_end(value_type, value_buffer)
                    yield self._process_value(current_key, value_type, value_buffer, first_value_token, last_value_token)
                    sys.stdout.flush()
                    first_value_token = False
                    if last_value_token:
                        key_patterns.pop(current_key)
                        reset_state()
                        
            # json_result = "".join(buffer).strip()
            # json_result = re.sub(r'^[^{]*', '', json_result)  # 一番左の { より左を削除
            # json_result = re.sub(r'}[^}]*$', '}', json_result)  # 一番右の } より右を削除

            # yield None, json_result

        return stream_json_values_generator()
