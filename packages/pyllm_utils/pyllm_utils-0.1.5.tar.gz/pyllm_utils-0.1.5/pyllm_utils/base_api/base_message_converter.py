from ..common_converter.data_encoder import DataEncoder
import copy

class BaseMessageConverter():
    def __init__(self):
        self.ALL_TYPES = ["audio_transcript", "audio", "image", "file_uri", "mime_type", "language", "code", "outcome", "output"]
        self.ALL_ROLES = ["user", "assistant", "tool", "model"]
        self.data_encoder = DataEncoder()
        self.ALLOWED_TYPES = []
        self.ALLOWED_ROLES = []
        
        
    def convert_request_messages(self, messages: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
        assert isinstance(messages, list) or messages is None, "messages must be a list or None"
        if messages is None:
            messages = []
        
        return [self._process_request_message(message) for message in messages]

    def _process_request_message(self, message: dict):
        pass