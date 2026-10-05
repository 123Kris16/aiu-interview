# CLI 模块

本模块提供命令行版本的智能体应用。

## 内容说明
- `agent_cli.py`：基于 Ollama 的命令行智能体，支持多轮对话与流式输出。

## 快速开始
```bash
python agent_cli.py
```
输入问题即可与智能体对话，输入 `退出` 结束程序。

## 依赖
- Requests
- Ollama（需提前启动并导入 `qwen2.5:7b`）

## 注意
本程序默认连接 `http://localhost:11434`，请确保 Ollama 正在运行。