"""
记忆管理服务封装。
负责读写本地 JSON 记忆文件，以及调用大模型做对话总结。
"""
import json
import os
import sys

# 将项目根目录加入路径，方便导入 llm 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.ollama_service import chat


MEMORY_FILE = "memory.json"
DEFAULT_MEMORY = "用户目前正在准备人工智能协会的面试，每天熬夜写代码，非常辛苦。"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"core_memory": DEFAULT_MEMORY, "chat_history": []}


def save_memory(core_memory, chat_history):
    data = {"core_memory": core_memory, "chat_history": chat_history}
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def summarize_memory(core_memory, chat_history):
    """
    当对话过长时，调用大模型对最近的对话进行总结，更新核心记忆。
    """
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history[-6:]])
    prompt = f"""
你是一个记忆总结助手。请根据以下最近对话记录，用一段话更新并总结用户的最新信息、偏好或近期状态。
这些总结将作为AI伴侣的永久记忆，请保持人设生动，用第二人称（你）来写。

【之前的核心记忆】：{core_memory}
【最近的对话记录】：
{history_text}

请直接输出更新后的核心记忆，不要加任何其他解释。
"""
    return chat([{"role": "user", "content": prompt}]).strip()