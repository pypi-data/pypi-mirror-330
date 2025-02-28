import re
from pathlib import Path

class DefaultDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

class PromptEditor:
    def __init__(self, template_source):
        if isinstance(template_source, str):
            self.template = template_source
        elif isinstance(template_source, Path):
            try:
                with open(template_source, 'r', encoding='utf-8') as file:
                    self.template = file.read()
            except Exception as e:
                raise ValueError(f"Failed to read template file: {e}")
        else:
            raise TypeError("template_source must be a file path or a string.")
        
        # 最も内側の中括弧以外を二重中括弧に変換
        self._converted_template = self._convert_nested_braces(self.template)
        self.processed_template = self.template
    
    def _convert_nested_braces(self, text):
        match = re.findall(r'\{[a-zA-Z_][a-zA-Z0-9_]*\}', text)
        #マッチ以外の中かっこを二重中かっこに変換
        text_parts = []
        last_end = 0
        for m in match:
            start = text.find(m, last_end)
            # マッチの前の部分を二重中かっこに変換
            prefix = text[last_end:start].replace('{', '{{').replace('}', '}}')
            text_parts.append(prefix)
            # マッチ部分はそのまま
            text_parts.append(m)
            last_end = start + len(m)
        # 最後の部分を二重中かっこに変換
        suffix = text[last_end:].replace('{', '{{').replace('}', '}}')
        text_parts.append(suffix)
        text = ''.join(text_parts)
        return text

    def apply(self, data):
        return self._converted_template.format_map(DefaultDict(data))
    
    def apply_processed(self, data):
        self._converted_processed_template = self._convert_nested_braces(self.processed_template)
        self.processed_template = self._converted_processed_template.format_map(DefaultDict(data))
        return self.processed_template
    
    def reset(self):
        self.processed_template = self.template