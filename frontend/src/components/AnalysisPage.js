import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function AnalysisPage() {
    const { eventId } = useParams();
    const [eventData, setEventData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/event/${eventId}`)
            .then(res => {
                if (!res.ok) throw new Error('Failed to fetch event');
                return res.json();
            })
            .then(data => {
                setEventData(data);
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching event:', err);
                setLoading(false);
            });
    }, [eventId]);

    if (loading) {
        return (
            <div style={{ 
                padding: '2rem',
                textAlign: 'center',
                minHeight: '100vh',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}>
                <p style={{ color: 'white', fontSize: '1.2rem' }}>Loading...</p>
            </div>
        );
    }

    if (!eventData) {
        return (
            <div style={{ 
                padding: '2rem',
                textAlign: 'center',
                minHeight: '100vh',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}>
                <p style={{ color: 'white', fontSize: '1.2rem' }}>Event not found</p>
                <Link to="/" style={{ color: 'white' }}>← Back to Dashboard</Link>
            </div>
        );
    }

    const eventSlug = eventData.slug || '';
    const markets = eventData.markets || [];
    
    // Check if it's a multi-outcome event (has groupItemTitle) or binary
    const isMultiOutcome = markets.length > 1 && markets[0].groupItemTitle;
    
    // Color palette for outcomes - more aesthetic pastels and vibrant colors
    const colors = [
        { bg: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', text: 'white' },  // Emerald
        { bg: 'linear-gradient(135deg, #f43f5e 0%, #e11d48 100%)', text: 'white' },  // Rose
        { bg: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)', text: 'white' },  // Indigo
        { bg: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', text: 'white' },  // Amber
        { bg: 'linear-gradient(135deg, #a855f7 0%, #9333ea 100%)', text: 'white' },  // Purple
        { bg: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)', text: 'white' }   // Cyan
    ];
    
    // Prepare outcomes data
    let outcomesData = [];
    if (isMultiOutcome) {
        // Multi-outcome: each market is an outcome
        outcomesData = markets.map(market => {
            const prices = JSON.parse(market.outcomePrices || '[0, 0]');
            return {
                label: market.groupItemTitle || market.question,
                price: (parseFloat(prices[0]) * 100).toFixed(1)
            };
        });
    } else {
        // Binary: single market with Yes/No
        const market = markets[0] || {};
        const outcomes = JSON.parse(market.outcomes || '["Yes", "No"]');
        const prices = JSON.parse(market.outcomePrices || '[0, 0]');
        outcomesData = outcomes.map((outcome, i) => ({
            label: outcome,
            price: (parseFloat(prices[i]) * 100).toFixed(1)
        }));
    }

    return (
        <div style={{ 
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            padding: '2rem'
        }}>
            <Link 
                to="/" 
                style={{
                    display: 'inline-block',
                    marginBottom: '1rem',
                    padding: '0.75rem 1.5rem',
                    background: 'rgba(255, 255, 255, 0.95)',
                    color: '#667eea',
                    textDecoration: 'none',
                    borderRadius: '8px',
                    fontWeight: '600',
                    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)'
                }}
            >
                ← Back to Dashboard
            </Link>

            {/* Market Display */}
            <div style={{
                background: 'rgba(255, 255, 255, 0.95)',
                borderRadius: '16px',
                padding: '2rem',
                maxWidth: '900px',
                margin: '0 auto 2rem auto',
                boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)'
            }}>
                <h1 style={{ color: '#2d3748', marginBottom: '1rem', fontSize: '1.8rem' }}>
                    {eventData.title}
                </h1>
                
                {eventData.image && (
                    <img 
                        src={eventData.image} 
                        alt={eventData.title}
                        style={{ 
                            width: '100%', 
                            maxHeight: '300px', 
                            objectFit: 'cover', 
                            borderRadius: '12px',
                            marginBottom: '1.5rem'
                        }}
                    />
                )}

                {/* Outcome Prices */}
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: outcomesData.length === 2 ? '1fr 1fr' : 'repeat(auto-fit, minmax(160px, 1fr))',
                    gap: '0.75rem',
                    marginBottom: '1.5rem'
                }}>
                    {outcomesData.map((outcome, index) => {
                        const color = colors[index % colors.length];
                        return (
                            <div key={index} style={{
                                background: color.bg,
                                padding: '1rem',
                                borderRadius: '10px',
                                textAlign: 'center',
                                color: color.text,
                                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
                            }}>
                                <div style={{ 
                                    fontSize: isMultiOutcome ? '0.75rem' : '0.85rem', 
                                    opacity: 0.95, 
                                    marginBottom: '0.4rem',
                                    fontWeight: '600',
                                    letterSpacing: '0.5px'
                                }}>
                                    {outcome.label.toUpperCase()}
                                </div>
                                <div style={{ fontSize: '2rem', fontWeight: '700' }}>{outcome.price}¢</div>
                            </div>
                        );
                    })}
                </div>

                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(3, 1fr)', 
                    gap: '1rem',
                    marginBottom: '1.5rem',
                    padding: '1rem',
                    background: '#f8fafc',
                    borderRadius: '8px'
                }}>
                    <div>
                        <div style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '0.25rem' }}>Volume</div>
                        <div style={{ fontSize: '1.1rem', fontWeight: '600', color: '#2d3748' }}>
                            ${(eventData.volumeNum || 0).toLocaleString()}
                        </div>
                    </div>
                    <div>
                        <div style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '0.25rem' }}>Liquidity</div>
                        <div style={{ fontSize: '1.1rem', fontWeight: '600', color: '#2d3748' }}>
                            ${(eventData.liquidityNum || 0).toLocaleString()}
                        </div>
                    </div>
                    <div>
                        <div style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '0.25rem' }}>24h Volume</div>
                        <div style={{ fontSize: '1.1rem', fontWeight: '600', color: '#2d3748' }}>
                            ${(eventData.volume24hr || 0).toLocaleString()}
                        </div>
                    </div>
                </div>

                <a 
                    href={`https://polymarket.com/event/${eventSlug}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                        display: 'block',
                        textAlign: 'center',
                        padding: '1rem',
                        background: '#667eea',
                        color: 'white',
                        textDecoration: 'none',
                        borderRadius: '8px',
                        fontWeight: '600',
                        transition: 'all 0.3s ease'
                    }}
                >
                    Trade on Polymarket →
                </a>
            </div>

            {/* Analysis Section Placeholder */}
            <div style={{
                background: 'rgba(255, 255, 255, 0.95)',
                borderRadius: '16px',
                padding: '3rem',
                maxWidth: '900px',
                margin: '0 auto',
                boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
                textAlign: 'center'
            }}>
                <h2 style={{ color: '#2d3748', marginBottom: '1rem' }}>
                    AI Analysis
                </h2>
                <p style={{ color: '#718096', fontSize: '1rem' }}>
                    Analysis coming soon...
                </p>
            </div>
        </div>
    );
}

export default AnalysisPage;