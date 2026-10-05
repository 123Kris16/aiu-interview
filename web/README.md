# Web 应用模块

本模块包含所有基于 Streamlit 的 Web 界面程序。

## 内容说明
- `app.py`：YOLO 图片检测 Web 应用。
- `chat_web.py`：本地大模型 Web 聊天界面。

## 快速开始

### 1. 运行 YOLO 检测网页
```bash
streamlit run app.py
```

### 2. 运行大模型聊天网页
```bash
streamlit run chat_web.py
```
两个应用都会在 `http://localhost:8501` 启动。

## 依赖
- Streamlit
- Ultralytics
- Requests
- Pillow
- Ollama（聊天页面需要）

## 注意
若端口 8501 被占用，Streamlit 会自动切换到其他端口，请留意终端提示。