from ultralytics import YOLO

model = YOLO('yolov8n.pt')
# Train the model
results = model.train(data='../Dataset/DFG_traffic_signal/JPEGImages/dataset_config.yaml', epochs=100, imgsz=640, device = 'mps')