from ultralytics import YOLO

# Load a pretrained YOLO model
model = YOLO('yolov8m-pose.pt')

video = 0

# Run inference on the source
results = model(source = video, show = True, conf = 0.3, save = True)