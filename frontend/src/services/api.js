const API_BASE = 'http://127.0.0.1:8000';

// Analysis endpoints
export const fetchEventAnalysis = async (eventId) => {
    const response = await fetch(`${API_BASE}/api/event/${eventId}/analysis`);
    if (!response.ok) {
        throw new Error('Failed to fetch event analysis');
    }
    return response.json();
};

export const fetchEventDetails = async (eventId) => {
    const response = await fetch(`${API_BASE}/api/event/${eventId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch event details');
    }
    return response.json();
};

// Home page endpoints
export const fetchTechEvents = async () => {
    try {
        const response = await fetch(`${API_BASE}/api/tech-events`);
        if (!response.ok) {
            throw new Error('Failed to fetch tech events');
        }
        const data = await response.json();
        return { data, error: null };
    } catch (err) {
        return { data: null, error: err.message };
    }
};

export const fetchTrendingEvents = async () => {
    try {
        const response = await fetch(`${API_BASE}/api/trending-events`);
        if (!response.ok) {
            throw new Error('Failed to fetch trending events');
        }
        const data = await response.json();
        return { data, error: null };
    } catch (err) {
        return { data: null, error: err.message };
    }
};

export const fetchSportsEvents = async () => {
    try {
        const response = await fetch(`${API_BASE}/api/sports-events`);
        if (!response.ok) {
            throw new Error('Failed to fetch sports events');
        }
        const data = await response.json();
        return { data, error: null };
    } catch (err) {
        return { data: null, error: err.message };
    }
};
