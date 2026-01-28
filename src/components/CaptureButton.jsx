import './CaptureButton.css';

const CaptureButton = ({ onClick, disabled }) => {
    return (
        <button
            className="capture-button btn-primary"
            onClick={onClick}
            disabled={disabled}
        >
            <span className="button-icon">📸</span>
            <span className="button-text">Capture Pothole</span>
        </button>
    );
};

export default CaptureButton;
