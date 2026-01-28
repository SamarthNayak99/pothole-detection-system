import { useState, useEffect } from 'react';

/**
 * Custom hook for accessing device GPS/location
 * @returns {Object} GPS state and coordinates
 */
export const useGPS = () => {
    const [coordinates, setCoordinates] = useState({
        latitude: null,
        longitude: null,
        accuracy: null
    });
    const [isActive, setIsActive] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!navigator.geolocation) {
            setError('Geolocation is not supported by your browser.');
            return;
        }

        let watchId;

        const startTracking = () => {
            watchId = navigator.geolocation.watchPosition(
                (position) => {
                    setCoordinates({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    });
                    setIsActive(true);
                    setError(null);
                },
                (err) => {
                    console.error('GPS error:', err);

                    if (err.code === err.PERMISSION_DENIED) {
                        setError('Location permission denied. Please allow location access.');
                    } else if (err.code === err.POSITION_UNAVAILABLE) {
                        setError('Location information unavailable.');
                    } else if (err.code === err.TIMEOUT) {
                        setError('Location request timed out.');
                    } else {
                        setError('Failed to get location.');
                    }

                    setIsActive(false);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        };

        startTracking();

        // Cleanup
        return () => {
            if (watchId) {
                navigator.geolocation.clearWatch(watchId);
            }
        };
    }, []);

    return {
        coordinates,
        isActive,
        error
    };
};
