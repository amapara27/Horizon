// frontend/src/services/api.js

const BACKEND_API = "http://127.0.0.1:8000";

/**
 * A robust helper function that *never* throws.
 * It always returns an object:
 * { data: <the_data>, error: null } on success
 * { data: null, error: <error_message> } on failure
 */
async function fetchFromBackend(endpoint) {
    try {
        const response = await fetch(`${BACKEND_API}${endpoint}`);
        
        if (!response.ok) {
            // Try to parse the error message from FastAPI
            try {
                const errorData = await response.json();
                const message = errorData.detail || `HTTP error! status: ${response.status}`;
                return { data: null, error: message }; // Return error
            } catch (jsonError) {
                // Fallback error
                return { data: null, error: `HTTP error! status: ${response.status}` };
            }
        }
        
        // Success case
        const data = await response.json();
        return { data: data, error: null }; // Return data

    } catch (networkError) {
        // This catches "Failed to fetch" if the backend is down
        // Convert error to string to avoid [Object Object]
        const errorMessage = networkError?.message || String(networkError) || "Network error occurred";
        return { data: null, error: errorMessage };
    }
}

// --- Exported API Functions ---
// These now pass the { data, error } object back to the component

export const fetchTechEvents = () => {
    return fetchFromBackend("/api/tech-events");
};

export const fetchTrendingEvents = () => {
    return fetchFromBackend("/api/trending-events");
};

export const fetchSportsEvents = () => {
    return fetchFromBackend("/api/sports-events");
};