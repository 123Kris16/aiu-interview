"""
Ollama 大语言模型服务封装。
对外提供统一的 chat 接口，供上层应用调用。
所有 Ollama API 调用都在这里完成，前端不需要直接接触 requests 库。
"""
import requests
import json


OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen2.5:7b"


def chat(messages, model=DEFAULT_MODEL):
    """
    非流式调用：一次性返回完整回复。
    messages 格式：[{"role": "system/user/assistant", "content": "..."}]
    """
    payload = {"model": model, "messages": messages, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        return f"调用大模型出错: {e}"


def stream_chat(messages, model=DEFAULT_MODEL):
    """
    流式调用：逐字生成器，供 Streamlit 的 st.write_stream 使用。
    """
    payload = {"model": model, "messages": messages, "stream": True}
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                decoded = json.loads(line.decode("utf-8").replace("data: ", ""))
                if "message" in decoded and "content" in decoded["message"]:
                    yield decoded["message"]["content"]
    except Exception as e:
        yield f"调用大模型出错: {e}"