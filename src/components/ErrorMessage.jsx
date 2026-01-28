import './ErrorMessage.css';

const ErrorMessage = ({ errors }) => {
    if (!errors || errors.length === 0) {
        return null;
    }

    return (
        <div className="error-container">
            {errors.map((error, index) => (
                <div key={index} className="error-card fade-in">
                    <span className="error-icon">⚠️</span>
                    <span className="error-text">{error}</span>
                </div>
            ))}
        </div>
    );
};

export default ErrorMessage;
