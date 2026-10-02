import requests
import json

SYSTEM_PROMPT = "你是一个人工智能协会创智部的专属智能体助手。你性格活泼、擅长技术，请用简洁清晰的中文回答问题。"

history = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat_with_agent_stream(user_input):
    history.append({"role": "user", "content": user_input})
    
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "qwen2.5:7b",
        "messages": history,
        "stream": True  # 关键修改：开启流式输出！
    }
    
    full_reply = ""
    print("\n智能体: ", end="", flush=True)
    try:
        # 使用 stream=True 持续接收数据
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                # 去掉前缀 "data: " 并解析 JSON
                decoded = json.loads(line.decode('utf-8').replace('data: ', ''))
                if 'message' in decoded and 'content' in decoded['message']:
                    chunk = decoded['message']['content']
                    full_reply += chunk
                    # 实时打印每一个字，flush=True 强制立即刷新屏幕
                    print(chunk, end="", flush=True)
        print() # 换行
        
    except Exception as e:
        print(f"\n连接本地大模型出错: {e}")
    
    history.append({"role": "assistant", "content": full_reply})

if __name__ == "__main__":
    print("🤖 你的专属本地智能体已启动！(输入 '退出' 结束对话)")
    print("提示：由于你的电脑没有独显，生成代码大概需要1-2分钟，请耐心等待它逐个字蹦出。")
    print("-" * 50)
    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input == "退出":
            print("智能体: 拜拜！")
            break
        chat_with_agent_stream(user_input)