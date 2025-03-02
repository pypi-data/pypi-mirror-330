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


class RawWebSearchAgent(Feature):
    """Google search feature implementation"""

    async def get_web_result(self, message: str, **kwargs):
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
                ans = wlanswer(content, message, k=kwargs.get("k", 1))
                res += f"Source: [{w.url}]\n\n{ans}\n"
                res += f"-" * 50 + "\n"
            except:
                pass
        return res

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):

        print(f'{kwargs=}')

        if kwargs.get("model") in HUGGINGCHAT_MODELS:
            api_key = "huggingchat"
        elif kwargs.get("model") in GPU_MODELS:
            api_key = "dsollama"
        else:
            api_key = "ollama"

        llm = LLM(api_key)

        from pydantic import BaseModel, Field

        class UserIntent(BaseModel):
            keywords: list[str]

        class Plan(BaseModel):
            plan: list[str]

        class Insights(BaseModel):
            three_key_findings: list[str] = Field(
                description="the findings for the answer , it can also be python code found")


        planner_prompt = (
            'Given user query, create a three stage websearch step-by-step plan in simple basic english minimal step each'
            ' the User query: {message}')

        plan: Plan = llm(planner_prompt.format(message=message),
                         response_format=Plan, model=kwargs.get("model")
                         )

        key_insights = ""
        for idx, step in enumerate(plan.plan):
            kwargs['k'] = 1
            # print(f'{step=}')
            step_result: str = await self.get_web_result(message=step, kwargs=kwargs)
            insights: Insights = llm(model=kwargs.get("model"),
                                     prompt=f'for [query] {step} [/query], given search result generate ONLY THREE insights , result: {step_result}',
                                     response_format=Insights)
            # print(f'{step_result=}')
            # print(insights)
            kp = "\n".join(insights.three_key_findings)
            key_insights += f'[STEP]{step}\n[INSIGHTS] {kp}\n'
            # print(f'{key_insights=}')

        answer = llm(
            f"Based on user question: {message}\n\n and the realtime resutls insgihts : {key_insights}\n, answer the user question",
            model=kwargs.get("model"))

        await handle_google_search(websocket=websocket,
                                   message=answer)
