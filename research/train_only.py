from ultralytics import YOLO
 
# Load the model.
model = YOLO('yolov8n.pt')
 
# Training.
results = model.train(
   data='custom_data_only.yaml',
   imgsz=1240,
   epochs=10,
   batch=16,
   name='yolov8n_custom_only')