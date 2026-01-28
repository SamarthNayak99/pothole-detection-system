import { useEffect } from 'react';
import './CameraFeed.css';

const CameraFeed = ({ videoRef, isActive, onStart }) => {
    useEffect(() => {
        // Auto-start camera when component mounts
        if (onStart && !isActive) {
            onStart();
        }
    }, [onStart, isActive]);

    return (
        <div className="camera-feed-container card">
            <h3>📹 Live Camera Feed</h3>
            <div className="video-wrapper">
                {!isActive && (
                    <div className="video-placeholder">
                        <div className="placeholder-icon">📷</div>
                        <p>Requesting camera access...</p>
                    </div>
                )}
                <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className={`video-element ${isActive ? 'active' : ''}`}
                />
            </div>
        </div>
    );
};

export default CameraFeed;
