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
        const bid = market.bestBid || 'N/A';
        const ask = market.bestAsk || 'N/A';
        const outcomes = JSON.parse(market.outcomes || '[]');
        const outcomeName = outcomes[0] || "Outcome 1";

        return (
            <div className="event-item">
                <div className="event-title">{title}</div>
                <div className="event-price">({outcomeName} Price: ${bid} / ${ask})</div>
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
    const [newEvents, setNewEvents] = useState({ data: null, error: null });
    const [trendingEvents, setTrendingEvents] = useState({ data: null, error: null });
    const [cryptoEvents, setCryptoEvents] = useState({ data: null, error: null });

    useEffect(() => {
        // Fetch data with proper error handling
        api.fetchNewEvents()
            .then(result => setNewEvents(result))
            .catch(err => setNewEvents({ data: null, error: String(err) }));
        
        api.fetchTrendingEvents()
            .then(result => setTrendingEvents(result))
            .catch(err => setTrendingEvents({ data: null, error: String(err) }));
        
        api.fetchCryptoEvents()
            .then(result => setCryptoEvents(result))
            .catch(err => setCryptoEvents({ data: null, error: String(err) }));
            
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
                    <h2>🚀 Newest Events</h2>
                    <div className="event-list">
                        <ColumnContent data={newEvents.data} error={newEvents.error} />
                    </div>
                </div>
                
                <div className="dashboard-column">
                    <h2>🔥 Trending Events</h2>
                    <div className="event-list">
                        <ColumnContent data={trendingEvents.data} error={trendingEvents.error} />
                    </div>
                </div>

                <div className="dashboard-column">
                    <h2>🪙 Crypto Events</h2>
                    <div className="event-list">
                        <ColumnContent data={cryptoEvents.data} error={cryptoEvents.error} />
                    </div>
                </div>
            </div>
        </>
    );
}

export default HomePage;