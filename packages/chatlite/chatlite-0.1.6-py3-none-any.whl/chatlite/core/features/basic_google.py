from fastapi import WebSocket
from liteutils import remove_references

from .base import Feature

import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI
import asyncio
from liteauto import compress,web


def streamer(res: str):
    "simulating streaming by using streamer"
    for i in range(0, len(res), 20):
        yield res[i:i + 20]


async def handle_google_search(websocket: WebSocket, message: str):
    """Handle Google search-like responses"""
    try:
        for chunk in streamer(message):
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

class FastGoogleSearch(Feature):
    """Google search feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None,**kwargs):
        # google_res = compress(web(message,max_urls=kwargs.get("is_websearch_k",3)),n=2)
        from liteauto import google,wlanswer
        from liteauto.parselite import aparse

        max_urls = kwargs.get("is_websearch_k", 3)
        print(f'{message=}')
        print(f'{max_urls=}')

        urls = google(message, max_urls=max_urls)
        print(f'{urls=}')

        web_results = await aparse(urls)
        web_results = [w for w in web_results if w.content]

        res = ""
        for w in web_results:
            try:
                if 'arxiv' in w.url:
                    content = remove_references(w.content)
                else:
                    content = w.content
                ans = wlanswer(content,message,k=2)
                res += f"Source: [{w.url}]\n\n{ans}\n"
                res += f"-"*50 + "\n"
            except:
                pass
        # google_res = compress(web_results,n=3)

        await handle_google_search(websocket=websocket,
                                   message=res)


