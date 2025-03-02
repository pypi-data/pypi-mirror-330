from .base import Feature
from fastapi import WebSocket

class EmailAssistantFeature(Feature):
    """Email assistant feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,**kwargs):
        system_prompt = "You are an email assistant. Help compose and format professional emails."
        await self.model_service.stream_response(websocket, message, system_prompt)