from .base import Feature
from ..model_service import ModelService

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI
import asyncio
from visionlite._vision_ai import visionai

def streamer(res):
    for x in res.split(" "):
        yield x+" "


async def handle_google_search(websocket: WebSocket, message: str,model_service:ModelService, system_prompt: str):
    """Handle Google search-like responses"""
    try:
        local_base_url = model_service.config.base_url.replace("/v1", "") if 'api' not in model_service.config.base_url else model_service.config.base_url
        google_res = visionai(message,
                              model=model_service.config.model_name,
                              base_url=local_base_url,
                              api_key=model_service.config.api_key)
        for chunk in streamer(google_res):
            await websocket.send_text(json.dumps({
                "sender": "bot",
                "message": chunk,
                "type": "stream"
            }))
            await asyncio.sleep(0.01)

        await websocket.send_text(json.dumps({
            "sender": "bot",
            "type": "end_stream"
        }))

    except Exception as e:
        await websocket.send_text(json.dumps({
            "sender": "bot",
            "message": f"Error: {str(e)}",
            "type": "error"
        }))

class RawWebSearchAgent(Feature):
    """Google search feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None,**kwargs):

        await handle_google_search(
            websocket,
            message,
            self.model_service,
            system_prompt
        )


