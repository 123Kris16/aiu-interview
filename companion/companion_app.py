"""
AI 伴侣主程序。
本文件只负责 UI 组织和模块组装，所有业务逻辑都委托给各服务模块。
"""
import streamlit as st
import sys
import os
from PIL import Image

# 将项目根目录加入路径，方便导入各模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.ollama_service import stream_chat
from yolo.yolo_service import YoloService
from companion.memory_service import load_memory, save_memory, summarize_memory


# ---------- 初始化服务 ----------
@st.cache_resource
def get_yolo():
    return YoloService()

yolo = get_yolo()


# ---------- 页面配置 ----------
st.set_page_config(page_title="专属AI伴侣", page_icon="💖", layout="centered")
st.title("💖 专属本地 AI 伴侣 (养成版)")
st.caption("纯本地运行，支持长期记忆、自动总结、图片场景感知。")


# ---------- 侧边栏 ----------
st.sidebar.header("⚙️ 伴侣设定")
with st.sidebar.expander("📝 基础设定", expanded=True):
    companion_name = st.text_input("她的名字", value="小雨")
    companion_desc = st.text_area(
        "性格与背景描述",
        value="你叫小雨，23岁，是一名插画师。你性格温柔、活泼，喜欢猫和咖啡。你说话时偶尔会带一个可爱的语气词。"
    )
    user_desc = st.text_input("你的设定（她怎么称呼你）", value="男神")


# ---------- 初始化状态 ----------
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "companion_messages" not in st.session_state:
    st.session_state.companion_messages = st.session_state.memory["chat_history"]
if "scenery_context" not in st.session_state:
    st.session_state.scenery_context = "你们正在通过网络聊天。"

with st.sidebar.expander("🧠 自动进化的核心记忆", expanded=True):
    st.write(st.session_state.memory["core_memory"])
    st.caption("（对话记录超过6条后，AI会自动总结并更新这里）")


# ---------- 历史消息 ----------
for msg in st.session_state.companion_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ---------- 图片上传 ----------
uploaded_file = st.file_uploader("📸 上传一张图片，让她了解你现在的环境...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="你分享的场景", use_container_width=True)
    with st.spinner("她正在看这张照片..."):
        detected = yolo.predict(image)
        if detected:
            st.session_state.scenery_context = f"你看到了我发给你的照片，照片里包含：{', '.join(detected)}。"
            st.success(f"👁️ 她看到了：{', '.join(detected)}")
        else:
            st.session_state.scenery_context = "你看到了我发的一张照片，但画面没有明显物体。"
            st.warning("没有识别出明显物体。")


# ---------- 聊天区域 ----------
st.divider()
st.subheader(f"💬 和 {companion_name} 的对话")

if prompt := st.chat_input(f"对 {companion_name} 说点什么..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.companion_messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        system_prompt = f"""
{companion_desc}
你正在和 {user_desc} 聊天。
【永久记忆】：{st.session_state.memory['core_memory']}
【当前场景】：{st.session_state.scenery_context}
请严格保持 {companion_name} 的人设和语气，结合永久记忆和当前场景，给出有情感、有逻辑的回复。
"""
        messages = [{"role": "system", "content": system_prompt}] + st.session_state.companion_messages
        full_response = st.write_stream(stream_chat(messages))
        st.session_state.companion_messages.append({"role": "assistant", "content": full_response})

        # 记忆自动总结
        if len(st.session_state.companion_messages) >= 6:
            with st.spinner("记忆正在进行压缩总结..."):
                new_core = summarize_memory(
                    st.session_state.memory["core_memory"],
                    st.session_state.companion_messages
                )
                st.session_state.memory["core_memory"] = new_core
                st.session_state.companion_messages = []
                st.success("✨ 记忆已自动压缩更新！")

        save_memory(
            st.session_state.memory["core_memory"],
            st.session_state.companion_messages
        )