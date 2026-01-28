import './CapturedGallery.css';

const CapturedGallery = ({ captures }) => {
    const formatTimestamp = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleString();
    };

    if (captures.length === 0) {
        return (
            <div className="gallery-container card">
                <h3>📷 Captured Potholes</h3>
                <div className="empty-state">
                    <div className="empty-icon">🕳️</div>
                    <p>No potholes captured yet</p>
                    <p className="empty-hint">Use the capture button to record potholes</p>
                </div>
            </div>
        );
    }

    return (
        <div className="gallery-container card">
            <h3>📷 Captured Potholes ({captures.length})</h3>
            <div className="gallery-grid">
                {captures.map((capture) => (
                    <div key={capture.id} className="capture-card fade-in">
                        <div className="capture-image-wrapper">
                            <img
                                src={capture.image}
                                alt="Captured pothole"
                                className="capture-image"
                            />
                        </div>
                        <div className="capture-info">
                            <div className="info-row">
                                <span className="info-label">📍 Location</span>
                                <span className="info-value">
                                    {capture.latitude.toFixed(6)}, {capture.longitude.toFixed(6)}
                                </span>
                            </div>
                            <div className="info-row">
                                <span className="info-label">🎯 Accuracy</span>
                                <span className="info-value">±{capture.accuracy.toFixed(0)}m</span>
                            </div>
                            <div className="info-row">
                                <span className="info-label">🕐 Time</span>
                                <span className="info-value">{formatTimestamp(capture.timestamp)}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CapturedGallery;
