# AIU 创智部二面实战项目

## 项目简介
本项目是参加人工智能协会创智部二面（实战部分）的完整工程记录。项目涵盖本地大模型部署、智能体开发、YOLO目标检测全流程以及多模态创意应用。所有代码、日志与文档均通过 Git 进行版本控制。

## 项目结构
```text
aiu-interview/
├── llm/                       # 大语言模型服务与配置
│   ├── ollama_service.py      # Ollama API 封装
│   ├── Modelfile              # 模型导入配置
│   └── README.md
├── yolo/                      # YOLO 目标检测
│   ├── yolo_service.py        # YOLO 推理服务封装
│   ├── realtime.py            # 实时摄像头推理
│   ├── yolo11n.pt             # 预训练权重
│   └── README.md
├── companion/                 # AI 伴侣创意作品
│   ├── companion_app.py       # 主程序（UI 组装）
│   ├── memory_service.py      # 记忆管理服务
│   └── README.md
├── web/                       # Streamlit Web 应用
│   ├── app.py                 # YOLO 检测网页
│   ├── chat_web.py            # 聊天网页
│   └── README.md
├── cli/                       # 命令行智能体
│   ├── agent_cli.py
│   └── README.md
├── docs/
│   └── journal.md             # 工程日志
├── datasets/                  # YOLO 训练数据集
├── runs/                      # YOLO 训练输出
├── memory.json                # AI 伴侣记忆存储（已被 .gitignore 忽略）
├── .gitignore
└── README.md
```

## 环境配置与依赖
本项目在 Windows 系统下开发，主要依赖以下工具：
- Python 环境管理：Miniforge3 (Python 3.14.7)
- 深度学习框架：Ultralytics 8.4.168, PyTorch 2.14.0 (CPU 版本)
- 大模型运行环境：Ollama 0.35.0
- 其他依赖：Streamlit, Requests, Pillow

### 快速安装
```bash
pip install ultralytics streamlit requests Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 启动命令
所有程序均从项目根目录运行：

```bash
# YOLO 图片检测 Web 应用
streamlit run web/app.py

# 大模型聊天 Web 应用
streamlit run web/chat_web.py

# AI 伴侣（创意作品）
streamlit run companion/companion_app.py

# 命令行智能体
python cli/agent_cli.py

# YOLO 实时摄像头推理
python yolo/realtime.py
```

## 各模块说明

### llm
负责本地大语言模型的部署与配置。使用 Ollama 导入 Qwen2.5-7B 模型，提供统一的 API 接口。
API 接入方式:
本项目采用前后端解耦架构。Ollama 作为本地 model provider，通过 HTTP API 对外提供模型推理服务，默认地址为 `http://localhost:11434/api/chat`。
应用层（Web / CLI / AI 伴侣）通过 `llm/ollama_service.py` 中封装的接口调用该 API，实现模型与应用完全解耦。若需切换到远程模型服务，只需修改该文件中的 URL，应用层代码无需改动。

### yolo
负责 YOLO 目标检测的训练、推理与模型管理。包含实时摄像头推理脚本和推理服务封装。

### companion
AI 伴侣创意作品。融合 YOLO 视觉感知、人格注入与 JSON 长期记忆，支持对话自动总结。

### web
所有基于 Streamlit 的 Web 界面程序，包括 YOLO 图片检测和本地大模型聊天。

### cli
命令行版智能体，支持多轮对话与流式输出。

## 踩坑记录与经验总结
1. GitHub / HuggingFace 访问受限：采用魔搭社区（ModelScope）下载 GGUF 模型和 coco8 数据集。
2. Ollama 分片模型导入报错：修改 Modelfile 中的路径为通配符 `*.gguf` 解决。
3. Streamlit DOM 渲染崩溃：改用原生 `st.write_stream` 接收生成器。
4. AI 伴侣记忆丢失：引入 JSON 持久化存储，并设计对话自动总结机制。
5. 模块化重构后导入路径失效：通过 `sys.path.append` 添加项目根目录解决。

## AI 使用情况说明
本项目在开发过程中使用了 AI 辅助编程（如生成基础代码框架、排查报错信息）。所有代码和踩坑解决方案均由本人亲自在本地环境测试通过，并记录了真实的工程日志。

## 作者
- GitHub: [@123Kris16](https://github.com/123Kris16)