import './GPSTracker.css';

const GPSTracker = ({ coordinates, isActive }) => {
    const formatCoordinate = (value) => {
        return value !== null ? value.toFixed(6) : '---';
    };

    return (
        <div className="gps-tracker-container card">
            <h3>🌍 GPS Coordinates</h3>
            <div className="coordinates-grid">
                <div className="coordinate-item">
                    <span className="coordinate-label">Latitude</span>
                    <span className="coordinate-value">
                        {formatCoordinate(coordinates.latitude)}°
                    </span>
                </div>

                <div className="coordinate-item">
                    <span className="coordinate-label">Longitude</span>
                    <span className="coordinate-value">
                        {formatCoordinate(coordinates.longitude)}°
                    </span>
                </div>

                <div className="coordinate-item">
                    <span className="coordinate-label">Accuracy</span>
                    <span className="coordinate-value">
                        {coordinates.accuracy !== null
                            ? `±${coordinates.accuracy.toFixed(0)}m`
                            : '---'}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default GPSTracker;
