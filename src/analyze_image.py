from ultralytics import YOLO

model = YOLO("yolov8n.pt")

image_path = "data/images/test.jpg"

results = model(image_path, save=True)

for result in results:
    print(result.boxes)