"""
命令行版智能体。
本文件只负责终端输入输出和调用 Ollama 服务。
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.ollama_service import stream_chat

SYSTEM_PROMPT = "你是一个人工智能协会创智部的专属智能体助手。你性格活泼、擅长技术，请用简洁清晰的中文回答问题。"

history = [{"role": "system", "content": SYSTEM_PROMPT}]

if __name__ == "__main__":
    print("🤖 专属智能体已启动！(输入 '退出' 结束对话)")
    print("-" * 50)
    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input == "退出":
            print("智能体: 拜拜！")
            break
        history.append({"role": "user", "content": user_input})
        print("\n智能体: ", end="", flush=True)
        full_reply = ""
        for chunk in stream_chat(history):
            print(chunk, end="", flush=True)
            full_reply += chunk
        print()
        history.append({"role": "assistant", "content": full_reply})