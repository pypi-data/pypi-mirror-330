import json
import pathlib
from .gemini_api.gemini_client import GeminiClient
from .anthropic_api.anthropic_client import AnthropicClient
from .openai_api.openai_client import OpenAIClient
from .llama_cpp_api.llama_cpp_client import LlamaCppClient

class LLMAPIClient:
    def __init__(self, model: str = "gpt-4o-mini", **kwargs):
        models_path = pathlib.Path(__file__).parent.resolve() / "models" / "models.json"
        local_models_path = pathlib.Path(__file__).parent.resolve() / "models" / "local_models.json"
        
        with open(models_path, "r", encoding="utf-8") as f:
            models = json.load(f)
        with open(local_models_path, "r", encoding="utf-8") as f:
            local_models = json.load(f)
        
        self.host = None
        for model_info in local_models.get("local_models", []):
            if model_info["name"] == model:
                self.host = "llama-cpp"
                break
        
        if not self.host:
            for model_info in models.get("openai", []):
                if model_info["name"] == model:
                    self.host = "openai"
                    break
            
            for model_info in models.get("anthropic", []):
                if model_info["name"] == model:
                    self.host = "anthropic"
                    break
                
            for model_info in models.get("google", []):
                if model_info["name"] == model:
                    self.host = "google"
                    break
            
        if self.host == "openai":
            self.client = OpenAIClient(model=model, **kwargs)
        elif self.host == "anthropic":
            self.client = AnthropicClient(model=model, **kwargs)
        elif self.host == "google":
            self.client = GeminiClient(model=model, **kwargs)
        elif self.host == "llama-cpp":
            self.client = LlamaCppClient(model=model, **kwargs)
        else:
            raise ValueError(f"Invalid model: {model}")
        
    def request_messages(self, **kwargs):
        return self.client.request_messages(**kwargs)
    
    def request_chat(self, **kwargs):
        return self.client.request_chat(**kwargs)
    
    def get_latest_response(self):
        return self.client.get_latest_response()
    
    def clear_chat_history(self):
        return self.client.clear_chat_history()

    def request_embeddings(self, input: str, model: str = "text-embedding-3-large"):
        return self.client.request_embeddings(input, model)
    
    async def async_request_embeddings(self, input: str, model: str = "text-embedding-3-large"):
        return self.client.request_embeddings(input, model)
    