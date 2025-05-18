from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Modelo de detección, no segmentación

model.train(
    data="data.yaml",
    epochs=200,
    imgsz=640
)