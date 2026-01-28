# Phase 2: Backend API Setup & Usage

## 📋 Overview

Simple FastAPI backend for the Pothole Detection System with:
- ✅ POST endpoint to save potholes
- ✅ GET endpoint to retrieve potholes
- ✅ CSV file storage (persistent)
- ✅ CORS enabled for frontend
- ❌ No ML, no authentication, no OpenCV

---

## 🚀 Installation & Setup

### Step 1: Install Python Dependencies

Open terminal in the `backend` folder and run:

```bash
pip install -r requirements.txt
```

This installs:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation

---

## ▶️ Running the Server

### Start the backend server:

```bash
uvicorn main:app --reload
```

**What this does:**
- Starts server on `http://localhost:8000`
- `--reload` enables auto-restart on code changes
- Creates `potholes.csv` file automatically

**You should see:**
```
🚀 Pothole Detection API started successfully!
📁 Using CSV file: potholes.csv
🌐 API available at: http://localhost:8000
📚 API docs at: http://localhost:8000/docs
```

---

## 📡 API Endpoints

### 1. Health Check
**GET** `/`

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "message": "Pothole Detection API is running",
  "version": "1.0.0"
}
```

---

### 2. Create Pothole
**POST** `/potholes`

**Request Body:**
```json
{
  "latitude": 37.774929,
  "longitude": -122.419418,
  "timestamp": "2025-12-29T15:30:00Z"
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:8000/potholes \
  -H "Content-Type: application/json" \
  -d '{"latitude": 37.774929, "longitude": -122.419418, "timestamp": "2025-12-29T15:30:00Z"}'
```

**Response:**
```json
{
  "id": 1,
  "latitude": 37.774929,
  "longitude": -122.419418,
  "timestamp": "2025-12-29T15:30:00Z"
}
```

---

### 3. Get All Potholes
**GET** `/potholes`

```bash
curl http://localhost:8000/potholes
```

**Response:**
```json
[
  {
    "id": 1,
    "latitude": 37.774929,
    "longitude": -122.419418,
    "timestamp": "2025-12-29T15:30:00Z"
  },
  {
    "id": 2,
    "latitude": 37.775123,
    "longitude": -122.419567,
    "timestamp": "2025-12-29T15:35:00Z"
  }
]
```

---

## 🧪 Testing the API

### Option 1: Interactive API Docs (Recommended)

1. Start the server
2. Open browser: `http://localhost:8000/docs`
3. You'll see Swagger UI with all endpoints
4. Click "Try it out" to test each endpoint

### Option 2: Using curl (Terminal)

```bash
# Test health check
curl http://localhost:8000/

# Create a pothole
curl -X POST http://localhost:8000/potholes \
  -H "Content-Type: application/json" \
  -d '{"latitude": 12.9716, "longitude": 77.5946, "timestamp": "2025-12-29T16:00:00Z"}'

# Get all potholes
curl http://localhost:8000/potholes
```

### Option 3: Using Python

```python
import requests

# Create pothole
response = requests.post(
    "http://localhost:8000/potholes",
    json={
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timestamp": "2025-12-29T16:00:00Z"
    }
)
print(response.json())

# Get all potholes
response = requests.get("http://localhost:8000/potholes")
print(response.json())
```

---

## 📁 Data Storage

**File:** `potholes.csv`

**Format:**
```csv
id,latitude,longitude,timestamp
1,37.774929,-122.419418,2025-12-29T15:30:00Z
2,37.775123,-122.419567,2025-12-29T15:35:00Z
```

**Location:** Same folder as `main.py`

**Notes:**
- File is created automatically on first run
- Data persists between server restarts
- Can be opened in Excel or any text editor

---

## 🔧 CORS Configuration

CORS is **enabled** to allow frontend (running on different port) to call the API.

Current settings (in `main.py`):
```python
allow_origins=["*"]  # Allow all origins (for development)
```

**For production**, change to specific origin:
```python
allow_origins=["http://localhost:5173"]  # Only allow your frontend
```

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## 📝 Code Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── potholes.csv        # Data storage (created automatically)
└── README.md           # This file
```

---

## ✅ Phase 2 Checklist

- [x] FastAPI backend created
- [x] POST /potholes endpoint
- [x] GET /potholes endpoint
- [x] CSV storage implemented
- [x] CORS enabled
- [x] Clean, commented code
- [x] Setup instructions provided
- [ ] Frontend integration (next step)

---

## 🎯 Next Steps

1. **Start the backend server** (see above)
2. **Test the API** using Swagger UI at `http://localhost:8000/docs`
3. **Update frontend** to call these endpoints instead of localStorage
4. **Phase 3**: Add ML model integration

---

## 🐛 Troubleshooting

**Error: "Port 8000 already in use"**
- Stop any other process using port 8000
- Or run on different port: `uvicorn main:app --reload --port 8001`

**Error: "Module not found"**
- Make sure you ran `pip install -r requirements.txt`
- Check you're in the correct directory

**CSV file not created**
- Check file permissions in the folder
- Server will create it automatically on first POST request

---

## 📚 Additional Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Uvicorn Docs: https://www.uvicorn.org/
- API Testing: http://localhost:8000/docs (Swagger UI)
