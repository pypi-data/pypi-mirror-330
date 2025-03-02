import asyncio
import json
from chatlite.core.config import ModelConfig
from openai import OpenAI
from fastapi import WebSocket

class ModelService:
    """Handles model interactions and streaming responses"""

    def __init__(self, config: ModelConfig):
        self.config = config
        self.client = OpenAI(
            base_url=config.base_url,
            api_key=config.api_key
        )

    async def stream_response(self, websocket: WebSocket, message: str, system_prompt: str,
                              chat_history=None,**kwargs):
        """Stream model responses"""
        try:
            print(f'{self.config=}')
            print(f"Starting stream with model: {self.config.model_name}")
            print(f"System prompt: {system_prompt}")
            print(f"User message: {message}")
            print()
            print(f'{kwargs=}')

            messages:list = [{"role": "system", "content": system_prompt}]

            if chat_history:
                messages.extend(chat_history)

            messages.append({"role": "user", "content": message})

            stream = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                stream=self.config.stream
            )

            for chunk in stream:
                if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                    # print(f"Streaming token: {chunk.choices[0].delta.content}")
                    await websocket.send_text(json.dumps({
                        "sender": "bot",
                        "message": chunk.choices[0].delta.content,
                        "type": "stream"
                    }))
                    await asyncio.sleep(0.01)

            await websocket.send_text(json.dumps({
                "sender": "bot",
                "type": "end_stream"
            }))
            print("Stream completed")

        except Exception as e:
            print(f"Error in streaming: {str(e)}")
            await websocket.send_text(json.dumps({
                "sender": "bot",
                "message": f"Error: {str(e)}",
                "type": "error"
            }))