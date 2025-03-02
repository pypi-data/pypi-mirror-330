from fastapi import WebSocket
from .base import Feature

import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI
import asyncio
from liteauto import compress,web

def streamer(res):
    for x in res.split(" "):
        yield x+" "


async def handle_google_search(websocket: WebSocket, message: str):
    """Handle Google search-like responses"""
    try:
        for chunk in streamer(message):
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

class FastGoogleSearch(Feature):
    """Google search feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None,**kwargs):
        # google_res = compress(web(message,max_urls=kwargs.get("is_websearch_k",3)),n=2)
        from liteauto import google
        from liteauto.parselite import aparse
        web_results = await aparse(google(message,max_urls=kwargs.get("is_websearch_k",3)))
        web_results = "\n".join([w.content for w in web_results if w.content])
        google_res = compress(web_results,n=3)

        await handle_google_search(websocket=websocket,
                                   message=google_res)

        # udpated_message = (f"### Google Result {google_res}\n"
        #                    f"using purely google results provide answer for user query: \n"
        #                    f"if results are youtube urls then return them as it is"
        #                    f"{message}")

        # await self.model_service.stream_response(websocket, udpated_message, system_prompt)


