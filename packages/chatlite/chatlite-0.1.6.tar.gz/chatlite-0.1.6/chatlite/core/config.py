from dataclasses import dataclass
from typing import Dict, Any, Optional


class ModelProvider:
    """Configuration mappings for different model providers"""

    # Base URLs for different providers
    BASE_URLS = {
        'local': "http://localhost:11434/v1",
        'huggingface': "https://api-inference.huggingface.co/v1/",
        'openai': "https://api.openai.com/v1"
    }

    # Default API keys
    DEFAULT_API_KEYS = {
        'local': "ollama",
        'huggingface': "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",
        'openai': None
    }

    # Default models for each provider
    DEFAULT_MODELS = {
        'local': "llama3.2:latest",
        'huggingface': "Qwen/Qwen2.5-72B-Instruct",
        'openai': "gpt-40-mini"
    }

    @classmethod
    def get_config(cls, model_type: str) -> Dict[str, Any]:
        """Get configuration for specified model type"""
        return {
            "base_url": cls.BASE_URLS[model_type],
            "api_key": cls.DEFAULT_API_KEYS[model_type],
            "default_model": cls.DEFAULT_MODELS[model_type]
        }

    def __repr__(self):
        return f"ModelProvider(BASE_URLS={self.BASE_URLS}, DEFAULT_API_KEYS={self.DEFAULT_API_KEYS}, DEFAULT_MODELS={self.DEFAULT_MODELS})"


@dataclass
class ModelConfig:
    """Configuration for language models"""
    model_type: str
    model_name: str
    base_url: str
    api_key: str
    temperature: float = 0.0
    max_tokens: int = 4000
    top_p: float = 0.75
    stream: bool = True

    @classmethod
    def create(cls,
               model_type: str,
               model_name: Optional[str] = None,
               api_key: Optional[str] = None,
               base_url: Optional[str] = None,
               **kwargs) -> 'ModelConfig':
        """Factory method to create ModelConfig with proper defaults"""
        provider_config = ModelProvider.get_config(model_type)

        return cls(
            model_type=model_type,
            model_name=model_name or provider_config["default_model"],
            base_url=base_url or provider_config["base_url"],
            api_key=api_key or provider_config["api_key"],
            **kwargs
        )

    def __repr__(self):
        return (f"ModelConfig(model_type={self.model_type!r}, "
                f"model_name={self.model_name!r}, "
                f"base_url={self.base_url!r}, "
                f"api_key={self.api_key!r}, "
                f"temperature={self.temperature!r}, "
                f"max_tokens={self.max_tokens!r}, "
                f"top_p={self.top_p!r}, "
                f"stream={self.stream!r})")

