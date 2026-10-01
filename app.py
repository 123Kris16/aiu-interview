import streamlit as st
from ultralytics import YOLO
from PIL import Image

# 设置网页标题
st.title("AIU 面试作品：YOLO 目标检测 Web 应用")

# 缓存加载模型，避免每次刷新都重新加载
@st.cache_resource
def load_model():
    return YOLO("runs/detect/train-2/weights/best.pt")

model = load_model()

# 网页上的文件上传组件
uploaded_file = st.file_uploader("请上传一张图片（支持 jpg, png）...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 把上传的文件转换成图片显示出来
    image = Image.open(uploaded_file)
    st.image(image, caption="你上传的图片", use_container_width=True)

    st.write("正在调用 YOLO 模型进行检测...")
    
    # 调用模型进行推理
    results = model.predict(image)
    
    # 把画好框的结果图提取出来
    annotated_image = results[0].plot()
    
    # 在网页上显示结果图
    st.image(annotated_image, caption="检测结果", use_container_width=True)
    st.success("🎉 检测完成！")