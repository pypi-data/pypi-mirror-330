# chatlite/__init__.py
import os
from typing import Optional
from chatlite.core._types._hf_type import HFModelType
from chatlite.core.config import ModelConfig
from chatlite.core import ChatServer

# Base server functionality
def create_server(
    model_type: str="local",
    model_name: Optional[HFModelType]|str = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 4000,
    base_url: Optional[str] = None,
    **kwargs
) -> ChatServer:
    """Create a unified server instance"""
    config = ModelConfig.create(
        model_type=model_type,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=base_url,
        **kwargs
    )
    return ChatServer(config)

def server(
    model_type: str="local",
    model_name: Optional[HFModelType]|str = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 4000,
    base_url: Optional[str] = None,
    **kwargs
):
    os.environ['OPENAI_API_KEY'] = api_key if api_key is not None else "ollama"
    os.environ['OPENAI_MODEL_NAME'] = model_name
    if base_url:
        os.environ['OPENAI_BASE_URL'] = base_url

    """Create a default server instance"""
    _app = create_server(
        model_type=model_type,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=base_url,
        **kwargs
    )
    _app.run()

# Local model functions
def local_qwen2p5(
    base_url="http://0.0.0.0:11434/v1",
    model_name="qwen2.5:0.5b-instruct",
    *args,
    **kwargs
):
    return server(
        model_type="local",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )

def local_llama3p2(
    base_url="http://0.0.0.0:11434/v1",
    model_name="llama3.2:latest",
    *args,
    **kwargs
):
    return server(
        model_type="local",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )

def local_qwen7b(
    base_url="http://0.0.0.0:11434/v1",
    model_name="qwen2.5:7b-instruct",
    *args,
    **kwargs
):
    return server(
        model_type="local",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )
def qwen7b(
    base_url="http://192.168.170.76:11434/v1",
    model_name="qwen2.5:7b-instruct",
    *args,
    **kwargs
):
    return server(
        model_type="local",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )

def deepseek_32b(
    base_url="http://192.168.170.76:11434/v1",
    model_name="hf.co/bartowski/DeepSeek-R1-Distill-Qwen-32B-abliterated-GGUF:Q5_K_M",
    *args,
    **kwargs
):
    return server(
        model_type="local",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )

def deepseek_14b(
    base_url="http://192.168.170.76:11434/v1",
    model_name="hf.co/bartowski/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q5_K_M",
    *args,
    **kwargs
):
    return server(
        model_type="local",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )

# HuggingFace models as direct callable functions
def _make_hf_caller(model_name: str):
    def caller(*args, **kwargs):
        return server(
            model_type='huggingface',
            model_name=model_name,
            api_key="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",
            *args,
            **kwargs
        )
    return caller

# Pre-configured HuggingFace models
mistral_7b_v3 = _make_hf_caller("mistralai/Mistral-7B-Instruct-v0.3")
mixtral_8x7b = _make_hf_caller("mistralai/Mixtral-8x7B-Instruct-v0.1")
qwen_72b = _make_hf_caller("Qwen/Qwen2.5-72B-Instruct")
qwen_32b_preview = _make_hf_caller("Qwen/QwQ-32B-Preview")
qwen_coder_32b = _make_hf_caller("Qwen/Qwen2.5-Coder-32B-Instruct")
hermes_8b = _make_hf_caller("NousResearch/Hermes-3-Llama-3.1-8B")
phi_mini = _make_hf_caller("microsoft/Phi-3.5-mini-instruct")
llama_8b = _make_hf_caller("meta-llama/Llama-3.1-8B-Instruct")
llama_1b = _make_hf_caller("meta-llama/Llama-3.2-1B-Instruct")
llama_3b = _make_hf_caller("meta-llama/Llama-3.2-3B-Instruct")
yi_34b = _make_hf_caller("01-ai/Yi-1.5-34B-Chat")
codellama_34b = _make_hf_caller("codellama/CodeLlama-34b-Instruct-hf")
gemma_7b = _make_hf_caller("google/gemma-1.1-7b-it")
gemma_2b = _make_hf_caller("google/gemma-2b-it")
starchat2_15b = _make_hf_caller("HuggingFaceH4/starchat2-15b-v0.1")
zephyr_7b = _make_hf_caller("HuggingFaceH4/zephyr-7b-beta")
llama2_7b = _make_hf_caller("meta-llama/Llama-2-7b-chat-hf")
llama3_70b = _make_hf_caller("meta-llama/Meta-Llama-3-70B-Instruct")
dialogpt = _make_hf_caller("microsoft/DialoGPT-medium")
phi_3_mini = _make_hf_caller("microsoft/Phi-3-mini-4k-instruct")
falcon_7b = _make_hf_caller("tiiuae/falcon-7b-instruct")

if __name__ == '__main__':
    local_qwen2p5()