"""
PHASE 3: Backend API for Pothole Detection System with ML
==========================================================

FastAPI backend with:
- POST /potholes - Save pothole data
- GET /potholes - Retrieve all potholes
- POST /detect - ML-based pothole detection from image
- CORS enabled for frontend access
- CSV storage + image storage
"""

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import csv
import os
from datetime import datetime
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import ML detector
from ml_detector import detect_pothole, get_detection_stats

# Import Email Notifier
try:
    from email_notifier import send_pothole_notification
except ImportError:
    print("⚠️ Email notifier not found or dependencies missing.")
    send_pothole_notification = None

# Initialize FastAPI app
app = FastAPI(
    title="Pothole Detection API",
    description="Backend API for storing and retrieving pothole locations",
    version="1.0.0"
)

# ============================================
# CORS Configuration
# ============================================
# Allow frontend to call backend from different origin (localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ============================================
# Static Files for Images
# ============================================
# Create directory if it doesn't exist
os.makedirs("detected_potholes", exist_ok=True)
# Mount static files to serve images
app.mount("/detected_potholes", StaticFiles(directory="detected_potholes"), name="detected_potholes")

# Data Models
# ============================================

class PotholeCreate(BaseModel):
    """Model for creating a new pothole entry"""
    latitude: float
    longitude: float
    timestamp: str
    confidence: Optional[float] = None  # ML confidence score
    image_path: Optional[str] = None    # Path to saved image
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 37.774929,
                "longitude": -122.419418,
                "timestamp": "2025-12-29T15:30:00Z",
                "confidence": 0.85,
                "image_path": "detected_potholes/pothole_20251229_153000_0.85.jpg"
            }
        }

class Pothole(BaseModel):
    """Model for pothole with ID"""
    id: int
    latitude: float
    longitude: float
    timestamp: str
    confidence: Optional[float] = None
    image_path: Optional[str] = None

class DetectionResult(BaseModel):
    """Model for ML detection result"""
    detected: bool
    confidence: float
    bbox: Optional[List[float]] = None
    image_filename: Optional[str] = None
    image_path: Optional[str] = None  # Full path with directory
    message: str

# ============================================
# CSV Storage Configuration
# ============================================

CSV_FILE = "potholes.csv"
CSV_HEADERS = ["id", "latitude", "longitude", "timestamp", "confidence", "image_path"]

def initialize_csv():
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        print(f"✅ Created new CSV file: {CSV_FILE}")

def get_next_id():
    """Get the next available ID for a new pothole"""
    if not os.path.exists(CSV_FILE):
        return 1
    
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            return 1
        return int(rows[-1]['id']) + 1

# ============================================
# API Endpoints
# ============================================

@app.get("/")
def read_root():
    """Root endpoint - API health check"""
    return {
        "message": "Pothole Detection API is running",
        "version": "1.0.0",
        "endpoints": {
            "POST /potholes": "Create new pothole entry",
            "GET /potholes": "Get all potholes"
        }
    }

@app.post("/potholes", response_model=Pothole, status_code=201)
def create_pothole(pothole: PotholeCreate):
    """
    Create a new pothole entry
    
    Args:
        pothole: PotholeCreate object with latitude, longitude, timestamp
        
    Returns:
        Pothole object with assigned ID
    """
    try:
        # Initialize CSV if needed
        initialize_csv()
        
        # Get next ID
        pothole_id = get_next_id()
        
        # Write to CSV
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                pothole_id,
                pothole.latitude,
                pothole.longitude,
                pothole.timestamp,
                pothole.confidence if pothole.confidence else "",
                pothole.image_path if pothole.image_path else ""
            ])
        
        print(f"✅ Pothole #{pothole_id} saved: ({pothole.latitude}, {pothole.longitude})")
        if pothole.confidence:
            print(f"   Confidence: {pothole.confidence:.2%}, Image: {pothole.image_path}")
            
            # Trigger Email Alert (Non-blocking)
            if send_pothole_notification:
                try:
                    # Run in background or just call (SMTP might delay response slightly)
                    print("📧 Initiating email alert...")
                    
                    # Ensure absolute path for image attachment
                    img_path = pothole.image_path
                    print(f"🔍 Original image path: {img_path}")
                    
                    if img_path:
                        # Convert to absolute path if relative
                        if not os.path.isabs(img_path):
                            img_path = os.path.abspath(img_path)
                            print(f"🔍 Converted to absolute path: {img_path}")
                        
                        # Verify file exists
                        if os.path.exists(img_path):
                            print(f"✅ Image file found at: {img_path}")
                        else:
                            print(f"❌ Image file NOT found at: {img_path}")
                            print(f"🔍 Current working directory: {os.getcwd()}")
                            # Try to find the file in detected_potholes folder
                            filename = os.path.basename(img_path)
                            alt_path = os.path.join(os.getcwd(), "detected_potholes", filename)
                            if os.path.exists(alt_path):
                                img_path = alt_path
                                print(f"✅ Found image at alternative path: {img_path}")
                            else:
                                print(f"❌ Alternative path also failed: {alt_path}")

                    send_pothole_notification(
                        pothole_id=pothole_id,
                        latitude=pothole.latitude,
                        longitude=pothole.longitude,
                        confidence=pothole.confidence,
                        timestamp=pothole.timestamp,
                        image_path=img_path
                    )
                except Exception as email_err:
                    print(f"⚠️ Email alert failed (but pothole saved): {email_err}")
                    import traceback
                    traceback.print_exc()
                
        # Return created pothole with ID
        return Pothole(
            id=pothole_id,
            latitude=pothole.latitude,
            longitude=pothole.longitude,
            timestamp=pothole.timestamp,
            confidence=pothole.confidence,
            image_path=pothole.image_path
        )
        
    except Exception as e:
        print(f"❌ Error saving pothole: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save pothole: {str(e)}")

@app.get("/potholes", response_model=List[Pothole])
def get_potholes():
    """
    Get all stored potholes
    
    Returns:
        List of all pothole entries
    """
    try:
        # Initialize CSV if needed
        initialize_csv()
        
        potholes = []
        
        # Read from CSV
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                potholes.append(Pothole(
                    id=int(row['id']),
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    timestamp=row['timestamp'],
                    confidence=float(row['confidence']) if row.get('confidence') and row['confidence'] else None,
                    image_path=row.get('image_path') if row.get('image_path') else None
                ))
        
        print(f"✅ Retrieved {len(potholes)} potholes")
        return potholes
        
    except Exception as e:
        print(f"❌ Error retrieving potholes: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve potholes: {str(e)}")

@app.delete("/potholes/{pothole_id}")
def delete_pothole(pothole_id: int):
    """
    Delete a pothole by ID
    
    Args:
        pothole_id: ID of the pothole to delete
        
    Returns:
        Success message
    """
    try:
        initialize_csv()
        
        # Read all potholes
        potholes = []
        pothole_to_delete = None
        
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['id']) == pothole_id:
                    pothole_to_delete = row
                else:
                    potholes.append(row)
        
        if not pothole_to_delete:
            raise HTTPException(status_code=404, detail=f"Pothole #{pothole_id} not found")
        
        # Write back without the deleted pothole
        with open(CSV_FILE, 'w', newline='') as f:
            fieldnames = ['id', 'latitude', 'longitude', 'timestamp', 'confidence', 'image_path']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(potholes)
        
        # Optionally delete the image file
        if pothole_to_delete.get('image_path'):
            image_path = pothole_to_delete['image_path']
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    print(f"🗑️ Deleted image: {image_path}")
                except Exception as img_err:
                    print(f"⚠️ Could not delete image: {img_err}")
        
        print(f"✅ Pothole #{pothole_id} deleted successfully")
        return {
            "message": f"Pothole #{pothole_id} deleted successfully",
            "deleted_id": pothole_id,
            "remaining_count": len(potholes)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error deleting pothole: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete pothole: {str(e)}")

@app.post("/detect", response_model=DetectionResult)
async def detect_pothole_endpoint(file: UploadFile = File(...)):
    """
    Detect pothole in uploaded image using YOLO ML model.
    
    Args:
        file: Uploaded image file
        
    Returns:
        DetectionResult with detection status, confidence, and image path
    """
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Run ML detection
        result = detect_pothole(image_bytes)
        
        if result["detected"]:
            return DetectionResult(
                detected=True,
                confidence=result["confidence"],
                bbox=result["bbox"],
                image_filename=result["image_filename"],
                image_path=result["image_path"],  # Full path with directory
                message=f"Pothole detected with {result['confidence']:.1%} confidence!"
            )
        else:
            return DetectionResult(
                detected=False,
                confidence=0.0,
                bbox=None,
                image_filename=None,
                image_path=None,
                message="No pothole detected in image."
            )
            
    except Exception as e:
        print(f"❌ Error in detection endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.get("/detection-stats")
def get_stats():
    """Get statistics about ML detections."""
    return get_detection_stats()


# ============================================
# Startup Event
# ============================================

@app.on_event("startup")
def startup_event():
    """Initialize CSV file on server startup"""
    initialize_csv()
    
    # Create detected_potholes directory if it doesn't exist
    os.makedirs("detected_potholes", exist_ok=True)
    
    print("🚀 Pothole Detection API started successfully!")
    print(f"📁 Using CSV file: {CSV_FILE}")
    print(f"🖼️  Images directory: detected_potholes/")
    print(f"🌐 API available at: http://localhost:8000")
    print(f"📚 API docs at: http://localhost:8000/docs")
