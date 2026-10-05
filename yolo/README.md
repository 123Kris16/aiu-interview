# YOLO 模块

本模块负责 YOLO 目标检测的训练、推理与模型管理。

## 内容说明
- `yolo11n.pt`：YOLO11n 预训练权重。
- `realtime.py`：实时摄像头推理脚本。
- 训练数据集与输出结果位于项目根目录的 `datasets/` 和 `runs/` 中。

## 快速开始

### 1. 实时摄像头推理
```bash
python realtime.py
```
按 `q` 键退出窗口。

### 2. 重新训练（可选）
```bash
yolo train model=yolo11n.pt data=coco8.yaml epochs=10 imgsz=640
```

## 依赖
- Ultralytics 8.4.168
- PyTorch 2.14.0（CPU 版本）
- OpenCV（用于摄像头读取）

## 注意
训练结果（权重、曲线图）会自动保存在 `runs/detect/` 下。