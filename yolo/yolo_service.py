"""
YOLO 目标检测服务封装。
对外提供 predict 接口，接收 PIL Image，返回识别到的物体名称列表。
"""
from ultralytics import YOLO
from PIL import Image


class YoloService:
    def __init__(self, model_path="yolo/yolo11n.pt"):
        self.model = YOLO(model_path)

    def predict(self, image: Image.Image):
        """
        输入：PIL Image 对象
        输出：识别到的物体名称列表（去重）
        """
        results = self.model.predict(image, verbose=False)
        class_names = results[0].names
        return list(set([class_names[int(cls)] for cls in results[0].boxes.cls]))