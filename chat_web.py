import streamlit as st
import requests
import json

st.set_page_config(page_title="AIU 专属智能体", page_icon="🤖", layout="centered")
st.title("🤖 AIU 创智部专属智能体")
st.caption("基于 Ollama + Qwen2.5，纯本地运行，支持多轮记忆与流式输出。")

# 定义系统人设
SYSTEM_PROMPT = "你是一个人工智能协会创智部的专属智能体助手。你性格活泼、擅长技术，请用简洁清晰的中文回答问题。"

# 初始化聊天历史（记忆功能）
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 侧边栏：显示状态 & 清空按钮
with st.sidebar:
    st.header("⚙️ 控制面板")
    st.write("当前模型：Qwen2.5-7B")
    st.write("运行模式：本地 CPU")
    if st.button("🗑️ 清空对话记录"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

# 渲染历史消息
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 用户输入框
if prompt := st.chat_input("请输入你的问题..."):
    # 1. 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 调用 Ollama 接口生成回答
    with st.chat_message("assistant"):
        # 使用生成器函数配合 st.write_stream 实现稳定的流式输出
        def stream_response():
            url = "http://localhost:11434/api/chat"
            payload = {
                "model": "qwen2.5:7b",
                "messages": st.session_state.messages,
                "stream": True
            }
            try:
                response = requests.post(url, json=payload, stream=True)
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        decoded = json.loads(line.decode('utf-8').replace('data: ', ''))
                        if 'message' in decoded and 'content' in decoded['message']:
                            yield decoded['message']['content']
            except Exception as e:
                yield f"连接本地大模型出错: {e}\n请确认 Ollama 正在运行。"

        # Streamlit 原生流式输出，彻底解决 React DOM 崩溃问题
        full_response = st.write_stream(stream_response())
        st.session_state.messages.append({"role": "assistant", "content": full_response})