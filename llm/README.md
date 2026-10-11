# LLM 模块

本模块负责本地大语言模型的部署与配置，以及文本转语音服务。

## 内容说明
- `ollama_service.py`：封装 Ollama API，提供 `chat` 和 `stream_chat` 接口。
- `tts_service.py`：封装 edge-tts，提供文本转语音服务。
- `Modelfile`：Ollama 模型导入配置，用于将 GGUF 格式的 Qwen2.5-7B 模型导入 Ollama。

## 快速开始

### 1. 导入模型
在项目根目录执行：
```bash
ollama create qwen2.5:7b -f llm/Modelfile
```
或者先进入 `llm` 目录：
```bash
cd llm
ollama create qwen2.5:7b -f Modelfile
```

### 2. 运行模型
```bash
ollama run qwen2.5:7b
```

### 3. 退出对话
输入 `/bye` 即可退出。

## 依赖
- Ollama 0.35.0 或更高版本
- Qwen2.5-7B-Instruct GGUF 模型文件
- edge-tts（文本转语音）

## 注意
本模块的 API 服务由 Ollama 在后台自动提供，默认端口 11434。