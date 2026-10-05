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

st.set_page_config(page_title="YOLO 目标检测", page_icon="🔍", layout="centered")
st.title("🔍 YOLO 目标检测 Web 应用")
st.caption("上传图片，YOLO 自动检测画面中的物体。")

@st.cache_resource
def get_yolo():
    return YoloService()

yolo = get_yolo()

uploaded_file = st.file_uploader("请上传一张图片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="你上传的图片", use_container_width=True)

    with st.spinner("正在检测..."):
        detected = yolo.predict(image)

    if detected:
        st.success(f"检测到：{', '.join(detected)}")
    else:
        st.warning("未检测到明显物体。")