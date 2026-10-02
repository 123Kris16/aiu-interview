# AIU 创智部二面实战项目

## 📖 项目简介
本项目是参加人工智能协会创智部二面（实战部分）的完整工程记录。项目涵盖**本地大模型部署**、**智能体开发**、**YOLO目标检测全流程**以及**多模态创意应用**。所有代码、日志与文档均通过 Git 进行版本控制。

## ✨ 核心功能与亮点

### 1. 本地大模型与智能体
- 基于 **Ollama** 本地部署 `Qwen2.5-7B` 大模型（纯 CPU 环境运行）。
- 实现 **CLI 智能体** (`agent_cli.py`) 与 **Web 聊天应用** (`chat_web.py`)。
- 支持流式输出（打字机效果）与多轮上下文记忆。

### 2. YOLO 目标检测全流程
- 完成 `Ultralytics` 官方 `coco8` 数据集的训练（`mAP50` 达到 0.85）。
- 实现 **实时摄像头推理** (`realtime.py`) 与 **Web 图片检测应用** (`app.py`)。
- 模型与数据集从魔搭社区（ModelScope）下载，规避了海外网络限制。

### 3. 创意作品：养成系 AI 伴侣 (`companion_app.py`)
- **多模态视觉感知**：使用 YOLO 提取图片中的物体标签，作为视觉场景上下文。
- **人格注入**：通过 System Prompt 自定义伴侣的名字、性格与语气。
- **长期记忆系统**：采用 `JSON` 本地持久化存储，结合大模型进行“对话自动总结”，实现长短期记忆的高效转换与自动进化。

## 📂 项目结构
```text
aiu-interview/
├── docs/
│   └── journal.md          # 详细工程日志（记录踩坑与解决方案）
├── datasets/               # YOLO 训练数据集（coco8）
├── runs/                   # YOLO 训练和推理结果（best.pt等）
├── app.py                  # YOLO Streamlit Web 应用
├── agent_cli.py            # 本地智能体 CLI 应用（对接 Ollama）
├── chat_web.py             # 智能体 Web 聊天界面（流式输出）
├── companion_app.py        # 创意作品：养成系 AI 伴侣
├── realtime.py             # YOLO 实时摄像头推理脚本
├── Modelfile               # Ollama 模型导入配置文件
├── yolo11n.pt              # YOLO 预训练权重
├── memory.json             # AI伴侣的记忆存储（已被 .gitignore 忽略）
└── README.md               # 项目说明文档
🛠️ 环境配置与依赖
本项目在 Windows 系统下开发，主要依赖以下工具：

Python 环境管理：Miniforge3 (Python 3.14.7)

深度学习框架：Ultralytics 8.4.168, PyTorch 2.14.0 (CPU 版本)

大模型运行环境：Ollama 0.35.0

其他依赖：Streamlit (Web界面), Requests (API调用), Pillow (图像处理)

快速安装
```bash
# 配置清华镜像源，保证下载速度
pip install ultralytics streamlit requests Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
🚀 使用说明
1. 运行 YOLO Web 应用
bash
streamlit run app.py
在浏览器中打开 http://localhost:8501，上传图片即可看到检测结果。

2. 运行智能体 Web 聊天
```bash
streamlit run chat_web.py
支持流式输出，自带人设设定与历史记忆。

3. 运行养成系 AI 伴侣 (创意作品)
```bash
streamlit run companion_app.py
先确保 Ollama 已启动。上传图片感知环境，输入文字与伴侣对话，体验记忆自动总结与长期进化。

4. YOLO 模型训练与实时推理
```bash
# 训练（coco8 数据集）
yolo train model=yolo11n.pt data=coco8.yaml epochs=10 imgsz=640

# 实时摄像头推理
python realtime.py
💡 踩坑记录与经验总结
在项目开发过程中，我遇到了许多国内网络环境和系统环境的挑战，以下是核心排障记录：

GitHub / HuggingFace 访问受限：

现象：下载模型和数据集时报错 SSL peer certificate 或 Connection timeout。

方案：采用魔搭社区（ModelScope）作为替代下载源，通过 modelscope download 命令成功拉取 GGUF 模型和 coco8 数据集，并通过配置 Git 代理解决了代码推送问题。

Ollama 分片模型导入报错：

现象：导入 qwen2.5-7b-instruct-q4_k_m 分片模型时提示 invalid split GGUF。

方案：修改 Modelfile 中的路径为通配符 *.gguf，让 Ollama 自动识别并合并分片。

Streamlit DOM 渲染崩溃：

现象：使用 st.empty() 配合手动更新实现流式输出时，触发 React removeChild 报错。

方案：改用 Streamlit 原生的 st.write_stream 接收生成器，完美解决。

AI伴侣记忆丢失：

现象：刷新网页后，聊天记录丢失，无法维持人格设定。

方案：引入 JSON 文件持久化存储，并设计“对话超过6条触发大模型自动总结”机制，实现了低成本的长期记忆管理。

🤖 AI 使用情况说明
本项目在开发过程中使用了 AI 辅助编程（如生成基础代码框架、排查报错信息）。

AI 主要用于加速信息检索和方案验证。所有代码和踩坑解决方案均由本人亲自在本地环境测试通过，并记录了真实的工程日志。

👤 作者
GitHub: @123Kris16
