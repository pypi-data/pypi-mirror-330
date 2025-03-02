import os
from concurrent.futures import ThreadPoolExecutor

from litegen import LLM
from pydantic import Field

from .base import Feature

from fastapi import WebSocket
from visionlite import visionai

from fastapi import WebSocket
from liteutils import remove_references

from .base import Feature

import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI, api_key
import asyncio
from liteauto import web, wlsplit

from liteauto import google, wlanswer
from liteauto.parselite import aparse

from ..model_names import HUGGINGCHAT_MODELS, GPU_MODELS


def streamer(res: str):
    "simulating streaming by using streamer"
    for i in range(0, len(res), 20):
        yield res[i:i + 20]

from litegen import LLMSearch


async def _handle_web_search(websocket: WebSocket, message: str):
    """Handle Google search-like responses"""
    llm_search = LLMSearch()
    try:
        for chunk in llm_search(message):
            await websocket.send_text(json.dumps({
                "sender": "bot",
                "message": chunk,
                "type": "stream"
            }))
            await asyncio.sleep(0.001)

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


class WebSearchAgent(Feature):
    """Google search feature implementation"""


    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):

        print(f'{kwargs=}')

        if kwargs.get("model") in HUGGINGCHAT_MODELS:
            api_key = "huggingchat"
        elif kwargs.get("model") in GPU_MODELS:
            api_key = "dsollama"
        else:
            api_key = "ollama"

        os.environ['OPENAI_API_KEY'] = api_key

        await _handle_web_search(websocket=websocket,
                                 message=message)
