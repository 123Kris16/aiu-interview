# AIU 创智部二面实战项目

## 📖 项目简介
本项目是参加人工智能协会创智部二面（实战部分）的完整工程记录。项目涵盖了**本地大模型部署**、**智能体开发**、**YOLO 目标检测全流程**，以及**Web 应用接入**。所有代码和文档均通过 Git 进行版本控制。

## 📂 项目结构
    aiu-interview/
    ├── docs/
    │   └── journal.md          # 详细工程日志（记录踩坑与解决方案）
    ├── datasets/               # YOLO 训练数据集（coco8）
    ├── runs/                   # YOLO 训练和推理结果（best.pt等）
    ├── app.py                  # YOLO Streamlit Web 应用
    ├── agent_cli.py            # 本地智能体 CLI 应用（对接 Ollama）
    ├── realtime.py             # YOLO 实时摄像头推理脚本
    ├── Modelfile               # Ollama 模型导入配置文件
    ├── yolo11n.pt              # YOLO 预训练权重
    └── README.md               # 项目说明文档

## 🛠️ 环境配置与依赖
本项目在 Windows 系统下开发，主要依赖以下工具：
- **Python 环境管理**：Miniforge3 (Python 3.14.7)
- **深度学习框架**：Ultralytics 8.4.168, PyTorch 2.14.0 (CPU 版本)
- **大模型运行环境**：Ollama 0.35.0
- **其他依赖**：Streamlit (Web 界面), Requests (API 调用)

### 快速安装
    # 配置清华镜像源，保证下载速度
    pip install ultralytics streamlit requests -i https://pypi.tuna.tsinghua.edu.cn/simple

## 🚀 使用说明

### 1. 运行 YOLO Web 应用
    streamlit run app.py
*在浏览器中打开 `http://localhost:8501`，上传图片即可看到检测结果。*

### 2. 运行本地智能体 CLI 应用
*请确保 Ollama 已在后台运行，并且已导入 `qwen2.5:7b` 模型。*
    python agent_cli.py
*支持多轮对话，采用流式输出，完美解决 CPU 推理慢导致的卡顿感。*

### 3. YOLO 模型训练与推理
    # 训练（coco8 数据集）
    yolo train model=yolo11n.pt data=coco8.yaml epochs=10 imgsz=640
    
    # 实时摄像头推理
    python realtime.py

## 💡 踩坑记录与经验总结（重点）
在项目开发过程中，我遇到了许多国内网络环境和系统环境的挑战，以下是核心排障记录：

1. **GitHub / HuggingFace 访问受限**：
   - 现象：下载模型和数据集时报错 `SSL peer certificate` 或 `Connection timeout`。
   - 方案：采用**魔搭社区（ModelScope）**作为替代下载源。通过 `modelscope download` 命令成功拉取 GGUF 模型和 coco8 数据集，并通过配置 Git 代理解决了代码推送问题。

2. **Ollama 分片模型导入报错**：
   - 现象：导入 `qwen2.5-7b-instruct-q4_k_m` 分片模型时提示 `invalid split GGUF`。
   - 方案：修改 `Modelfile` 中的路径为通配符 `*.gguf`，让 Ollama 自动识别并合并分片。

3. **CPU 推理大模型输出卡顿**：
   - 现象：使用 `stream=False` 时，由于纯 CPU 推理速度限制（2-5 token/s），生成较长代码时界面疑似“卡死”。
   - 方案：将 API 调用改为 `stream=True`，利用 `requests` 库实现逐字流式输出，大幅改善交互体验。

## 🤖 AI 使用情况说明
- 本项目在开发过程中使用了 AI 辅助编程（如生成基础代码框架、排查报错信息）。
- AI 主要用于加速信息检索和方案验证。所有代码和踩坑解决方案均由本人亲自在本地环境测试通过，并记录了真实的工程日志。

## 👤 作者
- GitHub: [@123Kris16](https://github.com/123Kris16)