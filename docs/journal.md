# 工程日志
## 2026-09-30
- 成功安装 Miniforge 和 Git。
- 配置了清华镜像源，解决了网络 SSL 报错问题。
- 完成了项目初始化。
## 2026-10-01
- 成功运行 YOLO 官方 coco8 数据集训练。
- 参数：yolo11n.pt, epochs=10, imgsz=640。
- 训练完成，生成结果保存在 runs/detect/train-2。
- 准确率评估：mAP50 达到 0.85。
- 踩坑记录：GitHub下载模型和数据集被墙，通过改用魔搭社区（ModelScope）手动下载解决。
## 2026-10-01 (下午)
- 最终成功实现了 YOLO 实时摄像头推理部署。
- 踩坑记录 1：Windows 下 OpenCV 弹窗可能静默失败（不报错也不弹窗），排查发现是代码修改后未在 VS Code 中按 Ctrl+S 保存，导致运行的是旧代码。教训：以后修改代码后第一件事就是保存，并观察终端是否有打印输出。
- 最终效果：摄像头实时检测，CPU 推理速度约 80-100ms/帧，成功识别出 person 和 refrigerator。
## 2026-10-01 (晚间)
- 使用 Streamlit 搭建了 YOLO 目标检测 Web 应用。
- 实现了图片上传、模型推理、结果展示的完整流程。
- 测试截图：终端成功识别出 2 persons, 1 cell phone。
- 至此，“任务二 YOLO” 全部完成。
## 2026-10-02
- 大模型部署：尝试 `ollama pull` 官方源下载，速度仅 18KB/s（预计耗时3小时），果断放弃。
- 解决方案：改用魔搭社区（ModelScope）命令行工具 `modelscope download` 下载 GGUF 格式模型（速度 3.6MB/s，耗时23分钟）。
- 踩坑记录：导入分片 GGUF 模型时，`ollama create` 报错 `invalid split GGUF`。通过修改 `Modelfile` 中的路径为通配符 `*`（如 `qwen2.5-7b-instruct-q4_k_m-*.gguf`），成功让 Ollama 自动合并分片。
- 最终结果：成功在本地运行 Qwen2.5-7B 模型，实现离线对话。
## 2026-10-02 (下午)
- 智能体开发完成，成功实现了多轮对话和上下文记忆。
- 踩坑记录：起初使用 `stream=False` 进行非流式请求，由于纯 CPU 环境运行 7B 模型（速度约 2-5 token/s），生成较长代码时界面长时间无反应，产生“卡死”错觉。
- 解决方案：将请求改为 `stream=True`，利用 requests 的流式读取和 `flush=True` 实现逐字输出，大幅提升交互体验，并成功生成了完整的 YOLO 检测代码。
## 2026-10-02 (Web应用篇)
- 将 Python CLI 智能体升级为 Streamlit Web 聊天界面 (chat_web.py)。
- 踩坑记录：起初使用 `st.empty()` 手动更新 DOM 节点实现打字机效果时，导致 React `removeChild` 崩溃报错。
- 解决方案：改用 Streamlit 原生的 `st.write_stream` 接收生成器，完美实现了流式输出和上下文记忆。
## 2026-10-02 (养成系AI伴侣篇)
- 完成创意作品：专属AI伴侣 (companion_app.py)。
- 核心功能：YOLO视觉感知、Streamlit Web界面、本地大模型对话。
- 引入长期记忆：通过JSON文件持久化存储，实现关掉浏览器后记忆不丢失。
- 实现记忆自动进化：当对话超过6条时，自动调用大模型进行摘要总结，更新核心记忆并清空短期记录，模拟人类“长短期记忆转换”机制。
- 踩坑记录：解决了Python变量作用域导致的 `NameError` 问题；解决了YOLO无法直接处理Streamlit字节流的问题（引入PIL）。