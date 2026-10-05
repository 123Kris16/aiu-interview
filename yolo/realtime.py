from ultralytics import YOLO

# 加载你刚刚训练好的模型
model = YOLO("runs/detect/train-2/weights/best.pt")

# 模式 A：打开摄像头实时检测
# 会弹出一个窗口显示画面，按键盘 'q' 键退出
results = model.predict(source=0, show=True, conf=0.5)

# 模式 B：如果没有摄像头，注释掉上面那行，取消下面这行的注释
# results = model.predict(source="https://ultralytics.com/images/bus.jpg", show=True)