from ultralytics import YOLO

#take the model from argument given in the command line

model = YOLO('yolov8n.pt')
dataset_config = '../Dataset/DFG_traffic_signal/JPEGImages/dataset_config.yaml'


if __name__=="__main__":
    # Train the model
    results = model.train(data=dataset_config, epochs=100, imgsz=640, device = 'mps')