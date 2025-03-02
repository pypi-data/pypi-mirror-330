from abc import ABC, abstractmethod

from fastapi import WebSocket

from ..model_names import HUGGINGCHAT_MODELS, GPU_MODELS
from ..model_service import ModelService
from ..config import ModelConfig




class Feature(ABC):
    """Base class for all chat features"""

    def __init__(self, model_service: ModelService):
        self.model_service: ModelService = model_service

    @abstractmethod
    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):
        """Handle the feature-specific logic"""
        pass


class DefaultChatFeature(Feature):
    """Default chat feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):
        if kwargs.get('model', None) in HUGGINGCHAT_MODELS:
            model_service = ModelService(ModelConfig(
                model_type="local",
                model_name=kwargs.get("model"),
                api_key=kwargs.get("api_key"),
                temperature=0.0,
                max_tokens=4000,
                base_url="http://localhost:11437/v1/",
            ))
        elif kwargs.get('model', None) in GPU_MODELS:
            model_service = ModelService(ModelConfig(
                model_type="local",
                model_name=kwargs.get("model"),
                api_key=kwargs.get("api_key"),
                temperature=0.0,
                max_tokens=4000,
                base_url="http://192.168.170.76:11434/v1/",
            ))
        else:
            model_service = self.model_service

        await model_service.stream_response(websocket, message, system_prompt, chat_history=chat_history, **kwargs)
