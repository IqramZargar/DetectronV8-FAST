from ultralytics import YOLO
import cv2
import os
import uuid

# Load model once at import time
model = YOLO("yolov8n.pt")


def run_detection(image_path: str, output_dir: str = "media/processed"):
    """
    Runs YOLOv8 detection on an input image, saves annotated image,
    and returns:
      1) output_path (str)
      2) detections (list[dict]) -> [{"label": "...", "confidence": 0.92}, ...]
    """
    os.makedirs(output_dir, exist_ok=True)

    results = model(image_path)

    detections = []
    for box in results[0].boxes:
        label = model.names[int(box.cls)]
        confidence = float(box.conf)
        detections.append(
            {
                "label": label,
                "confidence": round(confidence, 4),  # keep as decimal (0-1)
            }
        )

    annotated = results[0].plot()
    filename = f"{uuid.uuid4().hex}.jpg"
    output_path = os.path.join(output_dir, filename)
    cv2.imwrite(output_path, annotated)

    return output_path, detections