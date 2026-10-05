"""
文本转语音服务封装。
使用 edge-tts 将文字转为 mp3 文件，供前端播放。
"""
import edge_tts
import asyncio
import os

# 可选音色：zh-CN-XiaoxiaoNeural（温柔女声）、zh-CN-YunxiNeural（阳光男声）
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


def text_to_speech(text, output_path="temp_voice.mp3", voice=DEFAULT_VOICE):
    """
    将文字转换为语音文件，返回文件路径。
    如果生成失败，返回 None。
    """
    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

    try:
        asyncio.run(_generate())
        return output_path if os.path.exists(output_path) else None
    except Exception as e:
        print(f"TTS 生成失败: {e}")
        return None