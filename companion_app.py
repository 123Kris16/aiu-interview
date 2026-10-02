import streamlit as st
from ultralytics import YOLO
from PIL import Image
import requests
import json
import os

st.set_page_config(page_title="专属AI伴侣", page_icon="💖", layout="centered")
st.title("💖 专属本地 AI 伴侣 (养成版)")
st.caption("纯本地运行，支持长期记忆、自动总结、图片场景感知。")

MEMORY_FILE = "memory.json"

# 加载 YOLO 视觉模型
@st.cache_resource
def load_yolo():
    return YOLO("yolo11n.pt")
yolo_model = load_yolo()

# 读取记忆文件
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"core_memory": "用户目前正在准备人工智能协会的面试，每天熬夜写代码，非常辛苦。", "chat_history": []}

# 保存记忆文件
def save_memory(core_memory, chat_history):
    data = {"core_memory": core_memory, "chat_history": chat_history}
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 自动总结记忆
def summarize_memory(core_memory, chat_history):
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[-6:]])
    prompt = f"""
    你是一个记忆总结助手。请根据以下最近对话记录，用一段话更新并总结用户的最新信息、偏好或近期状态。
    这些总结将作为AI伴侣的永久记忆，请保持人设生动，用第二人称（你）来写。
    
    【之前的核心记忆】：{core_memory}
    【最近的对话记录】：
    {history_text}
    
    请直接输出更新后的核心记忆，不要加任何其他解释。
    """
    url = "http://localhost:11434/api/generate"
    payload = {"model": "qwen2.5:7b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        return response.json()['response'].strip()
    except Exception as e:
        print(f"总结记忆出错: {e}")
        return core_memory

# --- 侧边栏 ---
st.sidebar.header("⚙️ 伴侣设定")
with st.sidebar.expander("📝 基础设定", expanded=True):
    companion_name = st.text_input("她的名字", value="小雨")
    companion_desc = st.text_area(
        "性格与背景描述", 
        value="你叫小雨，23岁，是一名插画师。你性格温柔、活泼，喜欢猫和咖啡。你说话时偶尔会带一个可爱的语气词。"
    )
    user_desc = st.text_input("你的设定（她怎么称呼你）", value="男神")

# 初始化状态
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "companion_messages" not in st.session_state:
    st.session_state.companion_messages = st.session_state.memory["chat_history"]
# 🌟 初始化场景变量，解决未上传图片时的报错
if "scenery_context" not in st.session_state:
    st.session_state.scenery_context = "你们正在通过网络聊天。"

with st.sidebar.expander("🧠 自动进化的核心记忆", expanded=True):
    st.write(st.session_state.memory["core_memory"])
    st.caption("（对话记录超过6条后，AI会自动总结并更新这里）")

# 显示历史对话
for msg in st.session_state.companion_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 图片上传 ---
uploaded_file = st.file_uploader("📸 上传一张图片，让她了解你现在的环境...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="你分享的场景", use_container_width=True)
    
    with st.spinner('她正在看这张照片...'):
        results = yolo_model.predict(image)
        class_names = results[0].names
        detected_objects = list(set([class_names[int(cls)] for cls in results[0].boxes.cls]))
        
        if detected_objects:
            st.session_state.scenery_context = f"你看到了我发给你的照片，照片里包含：{', '.join(detected_objects)}。"
            st.success(f"👁️ 她看到了：{', '.join(detected_objects)}")
        else:
            st.session_state.scenery_context = "你看到了我发的一张照片，但画面有些模糊或没有明显物体。"
            st.warning("没有识别出明显物体。")

# --- 聊天区域 ---
st.divider()
st.subheader(f"💬 和 {companion_name} 的对话")

if prompt := st.chat_input(f"对 {companion_name} 说点什么..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.companion_messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        def stream_companion():
            system_prompt = f"""
            {companion_desc}
            你正在和 {user_desc} 聊天。
            【永久记忆】：{st.session_state.memory['core_memory']}
            【当前场景】：{st.session_state.scenery_context}
            请严格保持 {companion_name} 的人设和语气，结合永久记忆和当前场景，给出有情感、有逻辑的回复。
            """
            url = "http://localhost:11434/api/chat"
            payload = {
                "model": "qwen2.5:7b",
                "messages": [{"role": "system", "content": system_prompt}] + st.session_state.companion_messages,
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
                yield f"连接本地大模型出错: {e}"

        full_response = st.write_stream(stream_companion())
        st.session_state.companion_messages.append({"role": "assistant", "content": full_response})
        
        # 判断是否需要总结记忆
        if len(st.session_state.companion_messages) >= 6:
            with st.spinner("记忆正在进行压缩总结..."):
                new_core_memory = summarize_memory(
                    st.session_state.memory['core_memory'], 
                    st.session_state.companion_messages
                )
                st.session_state.memory['core_memory'] = new_core_memory
                st.session_state.companion_messages = []
                st.success("✨ 记忆已自动压缩更新！")
        
        # 保存记忆
        save_memory(st.session_state.memory['core_memory'], st.session_state.companion_messages)