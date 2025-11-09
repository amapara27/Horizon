// frontend/src/components/HomePage.js

import React, { useState, useEffect } from 'react';
import * as api from '../services/api';

/**
 * A helper component to render a single event.
 * (Unchanged)
 */
const EventItem = ({ event }) => {
    try {
        const market = event.markets[0];
        const title = event.title || 'N/A';
        const outcomes = JSON.parse(market.outcomes || '[]');
        
        // Get Yes and No prices
        const yesPrice = market.bestBid || 'N/A';
        const noPrice = market.bestAsk || 'N/A';

        return (
            <div className="event-item">
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
const ColumnContent = ({ error, data }) => {
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
    return data.map(event => <EventItem key={event.id} event={event} />);
};


/**
 * The main dashboard page
 */
function HomePage() {
    // State is now simpler, just data and error
    const [techEvents, setTechEvents] = useState({ data: null, error: null });
    const [trendingEvents, setTrendingEvents] = useState({ data: null, error: null });
    const [sportsEvents, setSportsEvents] = useState({ data: null, error: null });

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
                padding: '2rem 1rem 1rem 1rem',
                color: 'white'
            }}>
                <h1 style={{ 
                    fontSize: '2.5rem', 
                    fontWeight: '800',
                    margin: '0 0 0.5rem 0',
                    textShadow: '0 2px 10px rgba(0,0,0,0.2)'
                }}>
                    Horizon Dashboard
                </h1>
                <p style={{ 
                    fontSize: '1.1rem', 
                    opacity: '0.9',
                    margin: 0
                }}>
                    Real-time prediction market insights
                </p>
            </div>
            
            <div className="dashboard-container">
                <div className="dashboard-column">
                    <h2>💻 Tech Events</h2>
                    <div className="event-list">
                        <ColumnContent data={techEvents.data} error={techEvents.error} />
                    </div>
                </div>
                
                <div className="dashboard-column">
                    <h2>🔥 Trending Events</h2>
                    <div className="event-list">
                        <ColumnContent data={trendingEvents.data} error={trendingEvents.error} />
                    </div>
                </div>

                <div className="dashboard-column">
                    <h2>⚽ Sports Events</h2>
                    <div className="event-list">
                        <ColumnContent data={sportsEvents.data} error={sportsEvents.error} />
                    </div>
                </div>
            </div>
        </>
    );
}

export default HomePage;