"""
PHASE 3: ML Detection Module
=============================

YOLO-based pothole detection from images.
Processes frames from IP webcam and detects potholes.
"""

from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io
import os
from datetime import datetime

# Configuration
MODEL_PATH = "C:/Users/samar/Desktop/yolo_test/best.pt"
CONFIDENCE_THRESHOLD = 0.5  # 50% confidence minimum (balanced for real-world use)
# Use persistent disk for images in production, local directory in development
IMAGES_DIR = os.path.join(os.getenv("DATA_DIR", "."), "detected_potholes")

# Model will be loaded lazily (on first use)
model = None

def load_model():
    """Load YOLO model (lazy loading)"""
    global model
    if model is None:
        print("🔄 Loading YOLO model...")
        model = YOLO(MODEL_PATH)
        print(f"✅ YOLO model loaded from: {MODEL_PATH}")
        print(f"📊 Model classes: {model.names}")
        
        # Create images directory if it doesn't exist
        os.makedirs(IMAGES_DIR, exist_ok=True)
        print(f"📁 Images will be saved to: {IMAGES_DIR}")
    return model


def detect_pothole(image_bytes: bytes) -> dict:
    """
    Detect pothole in image using YOLO model.
    
    Args:
        image_bytes: Image data as bytes
        
    Returns:
        dict with detection results:
        {
            "detected": bool,
            "confidence": float,
            "bbox": [x1, y1, x2, y2],
            "image_path": str (if saved)
        }
    """
    try:
        # Load model if not already loaded
        current_model = load_model()
        
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB (remove alpha channel if present)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            print(f"🔄 Converted image from {image.mode} to RGB")
        
        # Convert PIL to numpy array for YOLO
        image_np = np.array(image)
        
        # Run YOLO detection
        results = current_model(image_np, conf=CONFIDENCE_THRESHOLD)
        
        # Debug: Print all detections
        print(f"🔍 Total detections: {len(results[0].boxes)}")
        if len(results[0].boxes) > 0:
            for i, box in enumerate(results[0].boxes):
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                print(f"   Detection {i+1}: Class={cls}, Confidence={conf:.2%}")
        
        # Check if any potholes detected
        if len(results[0].boxes) > 0:
            # Get first detection (highest confidence)
            box = results[0].boxes[0]
            confidence = float(box.conf[0])
            bbox = box.xyxy[0].cpu().numpy().tolist()  # [x1, y1, x2, y2]
            
            # Save image with detection
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"pothole_{timestamp}_{confidence:.2f}.jpg"
            image_path = os.path.join(IMAGES_DIR, image_filename)
            
            # Draw bounding box on image
            annotated_image = results[0].plot()  # YOLO's built-in visualization
            cv2.imwrite(image_path, annotated_image)
            
            print(f"✅ Pothole detected! Confidence: {confidence:.2%}, Saved: {image_filename}")
            
            return {
                "detected": True,
                "confidence": confidence,
                "bbox": bbox,
                "image_path": image_path,
                "image_filename": image_filename
            }
        else:
            # No pothole detected
            print(f"❌ No pothole detected (threshold: {CONFIDENCE_THRESHOLD:.0%})")
            return {
                "detected": False,
                "confidence": 0.0,
                "bbox": None,
                "image_path": None,
                "image_filename": None
            }
            
    except Exception as e:
        print(f"❌ Error in detection: {e}")
        raise Exception(f"Detection failed: {str(e)}")


def get_detection_stats() -> dict:
    """Get statistics about detected potholes."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(IMAGES_DIR, exist_ok=True)
        
        images = [f for f in os.listdir(IMAGES_DIR) if f.endswith('.jpg')]
        return {
            "total_detections": len(images),
            "images_directory": IMAGES_DIR
        }
    except Exception as e:
        return {
            "total_detections": 0,
            "images_directory": IMAGES_DIR,
            "error": str(e)
        }
