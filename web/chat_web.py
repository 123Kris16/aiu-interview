"""
大模型 Web 聊天界面。
本文件只负责 UI 组织和调用 Ollama 服务。
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.ollama_service import stream_chat

st.set_page_config(page_title="AIU 专属智能体", page_icon="🤖", layout="centered")
st.title("🤖 AIU 创智部专属智能体")
st.caption("基于 Ollama + Qwen2.5，纯本地运行。")

SYSTEM_PROMPT = "你是一个人工智能协会创智部的专属智能体助手。你性格活泼、擅长技术，请用简洁清晰的中文回答问题。"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

with st.sidebar:
    st.header("⚙️ 控制面板")
    if st.button("🗑️ 清空对话记录"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("请输入你的问题..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        full_response = st.write_stream(stream_chat(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": full_response})