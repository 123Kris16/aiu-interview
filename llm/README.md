# LLM 模块

本模块负责本地大语言模型的部署与配置。

## 内容说明
- `Modelfile`：Ollama 模型导入配置，用于将 GGUF 格式的 Qwen2.5-7B 模型导入 Ollama。

## 快速开始

### 1. 导入模型
确保已下载 GGUF 模型文件（位于项目根目录），然后执行：
```bash
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

## 注意
本模块的 API 服务由 Ollama 在后台自动提供，默认端口 11434。