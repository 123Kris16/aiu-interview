"""
YOLO 图片检测 Web 应用。
本文件只负责 UI 组织和调用 YoloService。
"""
import streamlit as st
import sys
import os
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from yolo.yolo_service import YoloService

st.set_page_config(page_title="YOLO 目标检测", page_icon="🔍", layout="wide")

# ---------- 自定义 CSS ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
        font-family: "Microsoft YaHei", sans-serif;
    }
    h1 {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 12px;
    }
    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        margin: 4px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔍 YOLO 目标检测 Web 应用")
st.caption("上传图片，YOLO 自动检测画面中的物体。")

@st.cache_resource
def get_yolo():
    return YoloService()

yolo = get_yolo()

uploaded_file = st.file_uploader("请上传一张图片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    image = Image.open(uploaded_file)

    with col1:
        st.image(image, caption="原图", use_container_width=True)

    with st.spinner("正在检测..."):
        results = yolo.model.predict(image, verbose=False)
        annotated = results[0].plot()
        class_names = results[0].names
        detected = list(set([class_names[int(cls)] for cls in results[0].boxes.cls]))
        confidences = [float(c) for c in results[0].boxes.conf]

    with col2:
        st.image(annotated, caption="检测结果", use_container_width=True)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    if detected:
        st.success(f"检测到 {len(results[0].boxes)} 个目标，共 {len(detected)} 类物体")
        tags_html = "".join([f'<span class="tag">{obj}</span>' for obj in detected])
        st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
        if confidences:
            avg_conf = sum(confidences) / len(confidences)
            st.metric("平均置信度", f"{avg_conf:.1%}")
    else:
        st.warning("未检测到明显物体。")
    st.markdown('</div>', unsafe_allow_html=True)