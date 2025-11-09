import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

const API_BASE = 'http://127.0.0.1:8000';

function AnalysisPage() {
    const { eventId } = useParams();
    const [eventData, setEventData] = useState(null);
    const [newsArticles, setNewsArticles] = useState([]);
    const [smartWallets, setSmartWallets] = useState([]);
    const [newsSentiment, setNewsSentiment] = useState(null);
    const [walletSentiment, setWalletSentiment] = useState(null);
    const [combinedSentiment, setCombinedSentiment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [analysisLoading, setAnalysisLoading] = useState(false);

    useEffect(() => {
        // Fetch event data
        fetch(`${API_BASE}/api/event/${eventId}`)
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

        // Fetch news articles
        fetch(`${API_BASE}/api/event/${eventId}/news`)
            .then(res => res.json())
            .then(data => {
                if (data.articles) {
                    setNewsArticles(data.articles);
                }
            })
            .catch(err => console.error('Error fetching news:', err));

        // Fetch smart wallets
        fetch(`${API_BASE}/api/event/${eventId}/smart-wallets`)
            .then(res => res.json())
            .then(data => setSmartWallets(data))
            .catch(err => console.error('Error fetching wallets:', err));
    }, [eventId]);

    const runAnalysis = async () => {
        setAnalysisLoading(true);
        
        try {
            // Fetch all three sentiment analyses
            const [newsRes, walletRes, combinedRes] = await Promise.all([
                fetch(`${API_BASE}/api/event/${eventId}/news-sentiment`),
                fetch(`${API_BASE}/api/event/${eventId}/wallet-sentiment`),
                fetch(`${API_BASE}/api/event/${eventId}/combined-sentiment`)
            ]);

            const newsData = await newsRes.json();
            const walletData = await walletRes.json();
            const combinedData = await combinedRes.json();

            setNewsSentiment(newsData);
            setWalletSentiment(walletData);
            setCombinedSentiment(combinedData);
        } catch (err) {
            console.error('Error running analysis:', err);
        } finally {
            setAnalysisLoading(false);
        }
    };

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

    const getSentimentColor = (score) => {
        if (score > 50) return '#16a34a';
        if (score > 20) return '#65a30d';
        if (score > -20) return '#ca8a04';
        if (score > -50) return '#ea580c';
        return '#dc2626';
    };

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

            {/* Three Column Layout */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 2fr 1fr',
                gap: '1.5rem',
                maxWidth: '1600px',
                margin: '0 auto 2rem auto'
            }}>
                {/* Left Section - News Articles */}
                <div style={{
                    background: 'rgba(255, 255, 255, 0.95)',
                    borderRadius: '16px',
                    padding: '2rem',
                    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
                    maxHeight: '600px',
                    overflowY: 'auto'
                }}>
                    <h3 style={{ color: '#2d3748', marginBottom: '1rem', fontSize: '1.2rem' }}>
                        📰 Related News
                    </h3>
                    {newsArticles.length > 0 ? (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                            {newsArticles.map((article, idx) => (
                                <a 
                                    key={idx}
                                    href={article.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    style={{
                                        background: 'linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%)',
                                        border: '1px solid #e2e8f0',
                                        borderRadius: '8px',
                                        padding: '0.75rem',
                                        textDecoration: 'none',
                                        color: 'inherit',
                                        transition: 'all 0.2s ease'
                                    }}
                                    onMouseEnter={(e) => {
                                        e.currentTarget.style.borderColor = '#667eea';
                                        e.currentTarget.style.transform = 'translateX(5px)';
                                    }}
                                    onMouseLeave={(e) => {
                                        e.currentTarget.style.borderColor = '#e2e8f0';
                                        e.currentTarget.style.transform = 'translateX(0)';
                                    }}
                                >
                                    <div style={{ 
                                        fontSize: '0.85rem',
                                        fontWeight: '600',
                                        color: '#2d3748',
                                        marginBottom: '0.5rem',
                                        lineHeight: '1.3'
                                    }}>
                                        {article.title}
                                    </div>
                                    <div style={{ 
                                        fontSize: '0.75rem',
                                        color: '#718096',
                                        marginBottom: '0.5rem'
                                    }}>
                                        {article.source}
                                    </div>
                                    {article.description && (
                                        <div style={{ 
                                            fontSize: '0.75rem',
                                            color: '#4a5568',
                                            lineHeight: '1.4'
                                        }}>
                                            {article.description.substring(0, 100)}...
                                        </div>
                                    )}
                                </a>
                            ))}
                        </div>
                    ) : (
                        <p style={{ color: '#718096', fontSize: '0.9rem' }}>Loading news articles...</p>
                    )}
                </div>

                {/* Center Section - Market Display (Thinner) */}
                <div style={{
                    background: 'rgba(255, 255, 255, 0.95)',
                    borderRadius: '16px',
                    padding: '2rem',
                    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)'
                }}>
                    <h1 style={{ color: '#2d3748', marginBottom: '1rem', fontSize: '1.5rem' }}>
                        {eventData.title}
                    </h1>
                    
                    {eventData.image && (
                        <img 
                            src={eventData.image} 
                            alt={eventData.title}
                            style={{ 
                                width: '100%', 
                                maxHeight: '200px', 
                                objectFit: 'cover', 
                                borderRadius: '12px',
                                marginBottom: '1rem'
                            }}
                        />
                    )}

                    {/* Outcome Prices */}
                    <div style={{ 
                        display: 'grid', 
                        gridTemplateColumns: outcomesData.length === 2 ? '1fr 1fr' : 'repeat(auto-fit, minmax(120px, 1fr))',
                        gap: '0.5rem',
                        marginBottom: '1rem'
                    }}>
                        {outcomesData.map((outcome, index) => {
                            const color = colors[index % colors.length];
                            return (
                                <div key={index} style={{
                                    background: color.bg,
                                    padding: '0.75rem',
                                    borderRadius: '8px',
                                    textAlign: 'center',
                                    color: color.text,
                                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
                                }}>
                                    <div style={{ 
                                        fontSize: '0.7rem', 
                                        opacity: 0.95, 
                                        marginBottom: '0.3rem',
                                        fontWeight: '600'
                                    }}>
                                        {outcome.label.toUpperCase()}
                                    </div>
                                    <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>{outcome.price}¢</div>
                                </div>
                            );
                        })}
                    </div>

                    <div style={{ 
                        display: 'grid', 
                        gridTemplateColumns: 'repeat(3, 1fr)', 
                        gap: '0.75rem',
                        marginBottom: '1rem',
                        padding: '0.75rem',
                        background: '#f8fafc',
                        borderRadius: '8px',
                        fontSize: '0.85rem'
                    }}>
                        <div>
                            <div style={{ fontSize: '0.7rem', color: '#64748b', marginBottom: '0.2rem' }}>Volume</div>
                            <div style={{ fontSize: '0.95rem', fontWeight: '600', color: '#2d3748' }}>
                                ${(eventData.volumeNum || 0).toLocaleString()}
                            </div>
                        </div>
                        <div>
                            <div style={{ fontSize: '0.7rem', color: '#64748b', marginBottom: '0.2rem' }}>Liquidity</div>
                            <div style={{ fontSize: '0.95rem', fontWeight: '600', color: '#2d3748' }}>
                                ${(eventData.liquidityNum || 0).toLocaleString()}
                            </div>
                        </div>
                        <div>
                            <div style={{ fontSize: '0.7rem', color: '#64748b', marginBottom: '0.2rem' }}>24h Volume</div>
                            <div style={{ fontSize: '0.95rem', fontWeight: '600', color: '#2d3748' }}>
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
                            padding: '0.75rem',
                            background: '#667eea',
                            color: 'white',
                            textDecoration: 'none',
                            borderRadius: '8px',
                            fontWeight: '600',
                            fontSize: '0.9rem'
                        }}
                    >
                        Trade on Polymarket →
                    </a>
                </div>

                {/* Right Section - Smart Wallets */}
                <div style={{
                    background: 'rgba(255, 255, 255, 0.95)',
                    borderRadius: '16px',
                    padding: '2rem',
                    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
                    maxHeight: '600px',
                    overflowY: 'auto'
                }}>
                    <h3 style={{ color: '#2d3748', marginBottom: '1rem', fontSize: '1.2rem' }}>
                        💼 Top Traders
                    </h3>
                    {smartWallets.length > 0 ? (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                            {smartWallets.map((wallet, idx) => (
                                <a
                                    key={idx}
                                    href={`https://polymarket.com/profile/${wallet.address}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    style={{
                                        background: 'linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%)',
                                        border: '1px solid #e2e8f0',
                                        borderRadius: '8px',
                                        padding: '0.75rem',
                                        fontSize: '0.85rem',
                                        textDecoration: 'none',
                                        color: 'inherit',
                                        transition: 'all 0.2s ease',
                                        display: 'block'
                                    }}
                                    onMouseEnter={(e) => {
                                        e.currentTarget.style.borderColor = '#667eea';
                                        e.currentTarget.style.transform = 'translateX(5px)';
                                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.2)';
                                    }}
                                    onMouseLeave={(e) => {
                                        e.currentTarget.style.borderColor = '#e2e8f0';
                                        e.currentTarget.style.transform = 'translateX(0)';
                                        e.currentTarget.style.boxShadow = 'none';
                                    }}
                                >
                                    <div style={{ 
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'center',
                                        marginBottom: '0.5rem'
                                    }}>
                                        <div style={{ 
                                            fontFamily: 'monospace', 
                                            fontSize: '0.75rem',
                                            color: '#4a5568',
                                            fontWeight: '600'
                                        }}>
                                            {wallet.address.substring(0, 6)}...{wallet.address.substring(38)}
                                        </div>
                                        <div style={{
                                            fontSize: '0.7rem',
                                            color: '#667eea',
                                            fontWeight: '600'
                                        }}>
                                            #{idx + 1}
                                        </div>
                                    </div>
                                    <div style={{ 
                                        display: 'flex', 
                                        justifyContent: 'space-between',
                                        marginBottom: '0.5rem',
                                        alignItems: 'center'
                                    }}>
                                        <span style={{
                                            padding: '0.25rem 0.5rem',
                                            borderRadius: '4px',
                                            background: wallet.position === 'YES' ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                            color: wallet.position === 'YES' ? '#16a34a' : '#dc2626',
                                            fontWeight: '700',
                                            fontSize: '0.75rem'
                                        }}>
                                            {wallet.position}
                                        </span>
                                        {wallet.position_strength && (
                                            <span style={{ 
                                                color: '#718096', 
                                                fontSize: '0.7rem',
                                                background: 'rgba(102, 126, 234, 0.1)',
                                                padding: '0.2rem 0.5rem',
                                                borderRadius: '4px'
                                            }}>
                                                {wallet.position_strength}% conviction
                                            </span>
                                        )}
                                    </div>
                                    <div style={{ 
                                        display: 'grid',
                                        gridTemplateColumns: '1fr 1fr',
                                        gap: '0.5rem',
                                        fontSize: '0.7rem',
                                        color: '#718096'
                                    }}>
                                        <div style={{ 
                                            background: 'rgba(102, 126, 234, 0.05)',
                                            padding: '0.3rem 0.5rem',
                                            borderRadius: '4px'
                                        }}>
                                            <div style={{ fontSize: '0.65rem', marginBottom: '0.1rem' }}>Volume</div>
                                            <div style={{ fontWeight: '600', color: '#4a5568' }}>
                                                ${wallet.size.toLocaleString()}
                                            </div>
                                        </div>
                                        <div style={{ 
                                            background: 'rgba(102, 126, 234, 0.05)',
                                            padding: '0.3rem 0.5rem',
                                            borderRadius: '4px'
                                        }}>
                                            <div style={{ fontSize: '0.65rem', marginBottom: '0.1rem' }}>Avg Price</div>
                                            <div style={{ fontWeight: '600', color: '#4a5568' }}>
                                                {wallet.entry_price}¢
                                            </div>
                                        </div>
                                    </div>
                                    {wallet.trade_count && (
                                        <div style={{ 
                                            marginTop: '0.5rem',
                                            fontSize: '0.7rem',
                                            color: '#9ca3af',
                                            textAlign: 'center'
                                        }}>
                                            {wallet.trade_count} trades
                                        </div>
                                    )}
                                </a>
                            ))}
                        </div>
                    ) : (
                        <p style={{ color: '#718096', fontSize: '0.9rem' }}>Loading trader data...</p>
                    )}
                </div>
            </div>

            {/* Bottom AI Analysis Section */}
            <div style={{
                background: 'rgba(255, 255, 255, 0.95)',
                borderRadius: '16px',
                padding: '2rem',
                maxWidth: '1600px',
                margin: '0 auto',
                boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)'
            }}>
                <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    marginBottom: '2rem'
                }}>
                    <h2 style={{ color: '#2d3748', margin: 0, fontSize: '1.5rem' }}>
                        🤖 AI Sentiment Analysis
                    </h2>
                    <button
                        onClick={runAnalysis}
                        disabled={analysisLoading}
                        style={{
                            padding: '0.75rem 1.5rem',
                            background: analysisLoading ? '#9ca3af' : '#667eea',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            fontWeight: '600',
                            cursor: analysisLoading ? 'not-allowed' : 'pointer',
                            fontSize: '0.9rem'
                        }}
                    >
                        {analysisLoading ? 'Analyzing...' : 'Run Analysis'}
                    </button>
                </div>

                {/* Three Analysis Subsections */}
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: '1.5rem'
                }}>
                    {/* News Sentiment - LEFT */}
                    <div style={{
                        background: 'linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%)',
                        border: '2px solid #e2e8f0',
                        borderRadius: '12px',
                        padding: '1.5rem',
                        textAlign: 'center'
                    }}>
                        <h3 style={{ color: '#2d3748', fontSize: '1rem', marginBottom: '1rem' }}>
                            📰 News Sentiment
                        </h3>
                        {newsSentiment ? (
                            <>
                                <div style={{
                                    fontSize: '3rem',
                                    fontWeight: '800',
                                    color: getSentimentColor(newsSentiment.sentiment_score),
                                    marginBottom: '0.5rem'
                                }}>
                                    {newsSentiment.sentiment_score > 0 ? '+' : ''}{newsSentiment.sentiment_score}%
                                </div>
                                <p style={{ 
                                    fontSize: '0.85rem', 
                                    color: '#4a5568',
                                    lineHeight: '1.5',
                                    textAlign: 'left'
                                }}>
                                    {newsSentiment.reasoning}
                                </p>
                            </>
                        ) : (
                            <p style={{ color: '#9ca3af', fontSize: '0.9rem' }}>
                                Click "Run Analysis" to start
                            </p>
                        )}
                    </div>

                    {/* Combined Sentiment - MIDDLE */}
                    <div style={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        border: '2px solid #5568d3',
                        borderRadius: '12px',
                        padding: '1.5rem',
                        textAlign: 'center',
                        color: 'white'
                    }}>
                        <h3 style={{ fontSize: '1rem', marginBottom: '1rem', opacity: 0.95 }}>
                            🎯 Overall Sentiment
                        </h3>
                        {combinedSentiment ? (
                            <>
                                <div style={{
                                    fontSize: '3rem',
                                    fontWeight: '800',
                                    marginBottom: '0.5rem'
                                }}>
                                    {combinedSentiment.sentiment_score > 0 ? '+' : ''}{combinedSentiment.sentiment_score}%
                                </div>
                                <div style={{
                                    display: 'inline-block',
                                    padding: '0.25rem 0.75rem',
                                    background: 'rgba(255, 255, 255, 0.2)',
                                    borderRadius: '12px',
                                    fontSize: '0.75rem',
                                    fontWeight: '600',
                                    marginBottom: '0.75rem',
                                    textTransform: 'uppercase'
                                }}>
                                    {combinedSentiment.confidence} confidence
                                </div>
                                <p style={{ 
                                    fontSize: '0.85rem',
                                    lineHeight: '1.5',
                                    textAlign: 'left',
                                    opacity: 0.95
                                }}>
                                    {combinedSentiment.reasoning}
                                </p>
                            </>
                        ) : (
                            <p style={{ opacity: 0.8, fontSize: '0.9rem' }}>
                                Click "Run Analysis" to start
                            </p>
                        )}
                    </div>

                    {/* Wallet Sentiment - RIGHT */}
                    <div style={{
                        background: 'linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%)',
                        border: '2px solid #e2e8f0',
                        borderRadius: '12px',
                        padding: '1.5rem',
                        textAlign: 'center'
                    }}>
                        <h3 style={{ color: '#2d3748', fontSize: '1rem', marginBottom: '1rem' }}>
                            💼 Smart Wallet Sentiment
                        </h3>
                        {walletSentiment ? (
                            <>
                                <div style={{
                                    fontSize: '3rem',
                                    fontWeight: '800',
                                    color: getSentimentColor(walletSentiment.sentiment_score),
                                    marginBottom: '0.5rem'
                                }}>
                                    {walletSentiment.sentiment_score > 0 ? '+' : ''}{walletSentiment.sentiment_score}%
                                </div>
                                <p style={{ 
                                    fontSize: '0.85rem', 
                                    color: '#4a5568',
                                    lineHeight: '1.5',
                                    textAlign: 'left'
                                }}>
                                    {walletSentiment.reasoning}
                                </p>
                            </>
                        ) : (
                            <p style={{ color: '#9ca3af', fontSize: '0.9rem' }}>
                                Click "Run Analysis" to start
                            </p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AnalysisPage;