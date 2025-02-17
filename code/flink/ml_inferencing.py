from ultralytics import YOLO
import numpy as np
def generate_volume(arrays:list[np.ndarray]):
    model = YOLO("yolov8n.pt")
    max_detections = 0
    for array in arrays:
        detections = __generate_unique_volume(model,array)
        max_detections = max(max_detections,detections)
    
    return max_detections
    
def __generate_unique_volume(model:YOLO,array:np.ndarray)->int:
    results = model.predict(array,verbose=False)
    boxes = results[0].boxes.numpy()
    human_id = 0
    detected_boxes = boxes.cls
    detections = 0
    for i in range(len(detected_boxes)):
        if detected_boxes[i] == human_id:
            detections += 1
            
    return detections


if __name__=="__main__":
    print("Python file for generating prediction")