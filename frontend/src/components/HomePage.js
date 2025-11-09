// frontend/src/components/HomePage.js

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import * as api from '../services/api';

/**
 * A helper component to render a single event.
 * (Unchanged)
 */
const EventItem = ({ event, onClick }) => {
    try {
        const market = event.markets[0];
        const title = event.title || 'N/A';
        
        // Get actual market prices from outcomePrices
        const outcomePrices = JSON.parse(market.outcomePrices || '[0, 0]');
        const yesPrice = parseFloat(outcomePrices[0]).toFixed(3);
        const noPrice = parseFloat(outcomePrices[1]).toFixed(3);

        return (
            <div className="event-item" onClick={() => onClick(event.id)}>
                <div className="event-title">{title}</div>
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                    <div className="event-price" style={{ background: 'rgba(34, 197, 94, 0.1)', color: '#16a34a' }}>
                        Yes: ${yesPrice}
                    </div>
                    <div className="event-price" style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#dc2626' }}>
                        No: ${noPrice}
                    </div>
                </div>
            </div>
        );
    } catch (e) {
        return null; 
    }
};

/**
 * NEW: A helper component to render a column's content
 * This now handles the new { data, error } state
 */
const ColumnContent = ({ error, data, onEventClick }) => {
    if (error) {
        // Convert error to string to prevent [Object Object]
        const errorMessage = typeof error === 'string' ? error : JSON.stringify(error);
        return <p className="loading error">Error: {errorMessage}</p>;
    }
    
    if (!data) {
        // Data is still loading (initial state is null)
        return <p className="loading">Loading...</p>;
    }

    if (data.length === 0) {
        // We got a successful response, but no events
        return <p className="loading">No events found.</p>;
    }

    // We have data, so we map it
    return data.map(event => <EventItem key={event.id} event={event} onClick={onEventClick} />);
};


/**
 * The main dashboard page
 */
function HomePage() {
    const navigate = useNavigate();
    
    // State is now simpler, just data and error
    const [techEvents, setTechEvents] = useState({ data: null, error: null });
    const [trendingEvents, setTrendingEvents] = useState({ data: null, error: null });
    const [sportsEvents, setSportsEvents] = useState({ data: null, error: null });

    const handleEventClick = (eventId) => {
        navigate(`/analysis/${eventId}`);
    };

    useEffect(() => {
        // Function to fetch all data
        const fetchAllData = () => {
            api.fetchTechEvents()
                .then(result => setTechEvents(result))
                .catch(err => setTechEvents({ data: null, error: String(err) }));
            
            api.fetchTrendingEvents()
                .then(result => setTrendingEvents(result))
                .catch(err => setTrendingEvents({ data: null, error: String(err) }));
            
            api.fetchSportsEvents()
                .then(result => setSportsEvents(result))
                .catch(err => setSportsEvents({ data: null, error: String(err) }));
        };

        // Fetch immediately on mount
        fetchAllData();

        // Set up auto-refresh every 30 seconds
        const interval = setInterval(fetchAllData, 30000);

        // Cleanup interval on unmount
        return () => clearInterval(interval);
    }, []); // Runs once on mount

    return (
        <>
            <div style={{ 
                textAlign: 'center', 
                padding: '3rem 1rem 2rem 1rem',
                background: '#1e293b',
                borderBottom: '1px solid #334155'
            }}>
                <h1 style={{ 
                    fontSize: '2.5rem', 
                    fontWeight: '800',
                    margin: '0 0 0.5rem 0',
                    color: '#f1f5f9',
                    letterSpacing: '-0.02em'
                }}>
                    Horizon Dashboard
                </h1>
                <p style={{ 
                    fontSize: '1.1rem', 
                    color: '#94a3b8',
                    margin: 0
                }}>
                    Real-time prediction market insights
                </p>
            </div>
            
            <div className="dashboard-container">
                <div className="dashboard-column">
                    <h2>💻 Tech Events</h2>
                    <div className="event-list">
                        <ColumnContent data={techEvents.data} error={techEvents.error} onEventClick={handleEventClick} />
                    </div>
                </div>
                
                <div className="dashboard-column">
                    <h2>🔥 Trending Events</h2>
                    <div className="event-list">
                        <ColumnContent data={trendingEvents.data} error={trendingEvents.error} onEventClick={handleEventClick} />
                    </div>
                </div>

                <div className="dashboard-column">
                    <h2>⚽ Sports Events</h2>
                    <div className="event-list">
                        <ColumnContent data={sportsEvents.data} error={sportsEvents.error} onEventClick={handleEventClick} />
                    </div>
                </div>
            </div>
        </>
    );
}

export default HomePage;