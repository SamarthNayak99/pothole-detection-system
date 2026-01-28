# 🚗 AI-Powered Pothole Detection System

A real-time pothole detection system using YOLO machine learning model, GPS tracking, and automated email alerts. Built with FastAPI backend and vanilla JavaScript frontend.

## 🌟 Features

- **🤖 AI Detection**: YOLO-based machine learning model for accurate pothole detection
- **📍 GPS Tracking**: Real-time location tracking with Google Maps integration
- **📧 Email Alerts**: Automatic notifications with image attachments
- **🗺️ Interactive Map**: View all detected potholes on an interactive map
- **📱 Mobile-First**: Optimized for mobile browsers with camera access
- **📊 History**: Track all detected potholes with timestamps and confidence scores
- **🎨 Modern UI**: Beautiful, responsive design with dark mode support

## 🚀 Live Demo

**Backend API**: [Your Railway URL here]
**Frontend**: [Your Vercel/Railway URL here]

## 📸 Screenshots

[Add screenshots of your app here]

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **YOLO (Ultralytics)** - Object detection ML model
- **OpenCV** - Image processing
- **Python 3.11** - Programming language

### Frontend
- **Vanilla JavaScript** - No frameworks, pure JS
- **HTML5/CSS3** - Modern web standards
- **Google Maps API** - Interactive mapping
- **Geolocation API** - GPS tracking

### Deployment
- **Railway** - Backend hosting
- **Vercel** - Frontend hosting (optional)
- **GitHub** - Version control

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend build)
- Git
- Gmail account (for email alerts)

## 🏃‍♂️ Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/pothole-detection-app.git
cd pothole-detection-app
```

### 2. Set Up Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:

```env
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECEIVER=receiver-email@gmail.com
```

Run the backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### 3. Set Up Frontend

```bash
npm install
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## 🌐 Deployment

See [RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md) for complete deployment instructions.

### Quick Deploy to Railway

1. Push to GitHub
2. Connect Railway to your repo
3. Add environment variables
4. Deploy!

## 📁 Project Structure

```
pothole-detection-app/
├── backend/
│   ├── main.py              # FastAPI backend
│   ├── ml_detector.py       # YOLO detection logic
│   ├── email_notifier.py    # Email alert system
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables (not in git)
│   └── detected_potholes/   # Saved images
├── src/
│   ├── components/          # React components (if using)
│   └── ...
├── public/
│   └── ...
├── detection.html           # Main detection page
├── map.html                 # Interactive map view
├── history.html             # Detection history
├── mobile-detect.html       # Mobile-optimized detection
├── package.json             # Node.js dependencies
├── requirements.txt         # Python dependencies (root)
├── railway.json             # Railway configuration
├── Procfile                 # Railway start command
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

Required environment variables for production:

```env
# Email Configuration
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_RECEIVER=receiver-email@gmail.com

# Server Configuration
PORT=8000
```

### Gmail App Password

To get a Gmail app password:
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Go to Security → App Passwords
4. Generate password for "Mail"
5. Use this password in `EMAIL_PASSWORD`

## 📊 API Endpoints

### POST /detect
Upload image for pothole detection

**Request**: Multipart form data with image file

**Response**:
```json
{
  "detected": true,
  "confidence": 0.85,
  "bbox": [x, y, width, height],
  "image_path": "detected_potholes/pothole_xxx.jpg",
  "message": "Pothole detected with 85.0% confidence!"
}
```

### POST /potholes
Save pothole data

**Request**:
```json
{
  "latitude": 12.9178647,
  "longitude": 77.4960684,
  "timestamp": "2026-01-22T15:09:16.758Z",
  "confidence": 0.85,
  "image_path": "detected_potholes/pothole_xxx.jpg"
}
```

### GET /potholes
Get all detected potholes

**Response**:
```json
[
  {
    "id": 1,
    "latitude": 12.9178647,
    "longitude": 77.4960684,
    "timestamp": "2026-01-22T15:09:16.758Z",
    "confidence": 0.85,
    "image_path": "detected_potholes/pothole_xxx.jpg"
  }
]
```

### DELETE /potholes/{id}
Delete a pothole by ID

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Your Name** - Initial work

## 🙏 Acknowledgments

- YOLO by Ultralytics for the ML model
- FastAPI for the amazing web framework
- Railway for easy deployment

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: your-email@example.com

## 🔮 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication
- [ ] Admin dashboard
- [ ] Pothole severity classification
- [ ] Route optimization for road maintenance
- [ ] Mobile app (React Native)
- [ ] Real-time notifications (WebSocket)
- [ ] Analytics dashboard

---

Made with ❤️ for safer roads
