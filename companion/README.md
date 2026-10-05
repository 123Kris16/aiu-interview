# AI 伴侣模块（创意作品）

本模块实现了一个具备视觉感知、人格注入与长期记忆的养成系 AI 伴侣。

## 内容说明
- `companion_app.py`：主程序，基于 Streamlit 的 Web 界面。
- 记忆文件 `memory.json` 位于项目根目录（已被 `.gitignore` 忽略）。

## 核心功能
- 视觉感知：通过 YOLO 识别图片中的物体，作为场景上下文。
- 人格注入：通过 System Prompt 自定义伴侣的名字、性格与语气。
- 长期记忆：使用 JSON 持久化存储，并在对话超过 6 条时自动总结更新。

## 快速开始
```bash
streamlit run companion_app.py
```
在浏览器中打开 `http://localhost:8501`。

## 依赖
- Streamlit
- Requests
- Pillow
- Ollama（需提前启动并导入 `qwen2.5:7b`）
- YOLO（需提前安装 ultralytics）

## 注意
首次运行会自动创建 `memory.json`，请勿手动删除，否则记忆会丢失。
