"""
Test Backend Connection and ML Model
"""
import requests
import json

API_URL = "http://10.42.117.136:8000"

print("=" * 60)
print("BACKEND TESTING SCRIPT")
print("=" * 60)

# Test 1: Check if backend is running
print("\n1️⃣ Testing backend connection...")
try:
    response = requests.get(f"{API_URL}/")
    print(f"✅ Backend is running!")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Backend connection failed: {e}")
    print("   Make sure backend is running: uvicorn main:app --reload")
    exit(1)

# Test 2: Check if ML model is loaded
print("\n2️⃣ Testing ML detection endpoint...")
try:
    # Create a dummy image file
    import io
    from PIL import Image
    import numpy as np
    
    # Create a test image (black square)
    img = Image.new('RGB', (640, 640), color='black')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Send to detection endpoint
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    response = requests.post(f"{API_URL}/detect", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ ML detection endpoint working!")
        print(f"   Response: {json.dumps(result, indent=2)}")
    else:
        print(f"❌ Detection failed with status: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ ML detection test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check potholes endpoint
print("\n3️⃣ Testing potholes endpoint...")
try:
    response = requests.get(f"{API_URL}/potholes")
    if response.status_code == 200:
        potholes = response.json()
        print(f"✅ Potholes endpoint working!")
        print(f"   Total potholes in database: {len(potholes)}")
        if potholes:
            print(f"   Latest pothole: {potholes[-1]}")
    else:
        print(f"❌ Failed with status: {response.status_code}")
except Exception as e:
    print(f"❌ Potholes endpoint test failed: {e}")

print("\n" + "=" * 60)
print("TESTING COMPLETE")
print("=" * 60)
