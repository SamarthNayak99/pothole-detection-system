import { useState } from 'react';
import { useCamera } from './hooks/useCamera';
import { useGPS } from './hooks/useGPS';
import StatusIndicator from './components/StatusIndicator';
import CameraFeed from './components/CameraFeed';
import GPSTracker from './components/GPSTracker';
import CaptureButton from './components/CaptureButton';
import CapturedGallery from './components/CapturedGallery';
import ErrorMessage from './components/ErrorMessage';
import './App.css';

function App() {
  const [captures, setCaptures] = useState([]);
  const { videoRef, isActive: cameraActive, error: cameraError, startCamera } = useCamera();
  const { coordinates, isActive: gpsActive, error: gpsError } = useGPS();

  const handleCapture = () => {
    if (!videoRef.current || !cameraActive) {
      return;
    }

    // Create canvas to capture frame
    const canvas = document.createElement('canvas');
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    // Convert to image data
    const imageData = canvas.toDataURL('image/jpeg', 0.8);

    // Create capture object
    const newCapture = {
      id: Date.now(),
      image: imageData,
      latitude: coordinates.latitude || 0,
      longitude: coordinates.longitude || 0,
      accuracy: coordinates.accuracy || 0,
      timestamp: new Date().toISOString()
    };

    // Add to captures array
    setCaptures(prev => [newCapture, ...prev]);
  };

  // Collect all errors
  const errors = [cameraError, gpsError].filter(Boolean);

  return (
    <div className="app">
      <div className="container">
        <header className="app-header">
          <h1>🕳️ Pothole Detection System</h1>
          <p className="app-subtitle">
            Crowdsourced road monitoring using camera and GPS
          </p>
        </header>

        <ErrorMessage errors={errors} />

        <StatusIndicator
          cameraActive={cameraActive}
          gpsActive={gpsActive}
        />

        <div className="main-content">
          <CameraFeed
            videoRef={videoRef}
            isActive={cameraActive}
            onStart={startCamera}
          />

          <GPSTracker
            coordinates={coordinates}
            isActive={gpsActive}
          />

          <CaptureButton
            onClick={handleCapture}
            disabled={!cameraActive || !gpsActive}
          />
        </div>

        <CapturedGallery captures={captures} />

        <footer className="app-footer">
          <p>Phase 1: Frontend Demo - Camera & GPS Integration</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
