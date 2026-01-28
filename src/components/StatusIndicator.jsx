import './StatusIndicator.css';

const StatusIndicator = ({ cameraActive, gpsActive }) => {
    return (
        <div className="status-container">
            <div className={`status-badge ${cameraActive ? 'active' : 'inactive'}`}>
                <span className="status-dot"></span>
                <span className="status-text">
                    Camera: {cameraActive ? 'Active' : 'Inactive'}
                </span>
            </div>

            <div className={`status-badge ${gpsActive ? 'active' : 'inactive'}`}>
                <span className="status-dot"></span>
                <span className="status-text">
                    GPS: {gpsActive ? 'Locked' : 'Searching...'}
                </span>
            </div>
        </div>
    );
};

export default StatusIndicator;
