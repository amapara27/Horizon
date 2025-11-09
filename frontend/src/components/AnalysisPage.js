import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchEventAnalysis, fetchEventDetails } from '../services/api';

function AnalysisPage() {
    const { eventId } = useParams();
    const [eventData, setEventData] = useState(null);
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedOutcome, setSelectedOutcome] = useState(0);

    useEffect(() => {
        loadEventData();
    }, [eventId]);

    const loadEventData = async () => {
        try {
            setLoading(true);
            setError(null);
            
            const [details, analysisData] = await Promise.all([
                fetchEventDetails(eventId),
                fetchEventAnalysis(eventId)
            ]);
            
            setEventData(details);
            setAnalysis(analysisData);
        } catch (err) {
            console.error('Error loading event data:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const getScoreColor = (score) => {
        if (score >= 70) return '#10b981';
        if (score >= 50) return '#84cc16';
        if (score >= 30) return '#f59e0b';
        if (score >= 10) return '#f97316';
        return '#ef4444';
    };

    const getSentimentColor = (score) => {
        if (score > 50) return '#10b981';
        if (score > 0) return '#84cc16';
        if (score === 0) return '#64748b';
        if (score > -50) return '#f97316';
        return '#ef4444';
    };

    if (loading) {
        return (
            <div style={{ 
                minHeight: '100vh', 
                background: '#0f172a',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                <div style={{ fontSize: '1.5rem', color: '#64748b' }}>Loading analysis...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ 
                minHeight: '100vh', 
                background: '#0f172a',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexDirection: 'column',
                gap: '1rem'
            }}>
                <div style={{ fontSize: '1.5rem', color: '#ef4444' }}>Error</div>
                <div style={{ color: '#64748b' }}>{error}</div>
                <Link to="/" style={{ color: '#6366f1', textDecoration: 'none' }}>
                    ← Back to Home
                </Link>
            </div>
        );
    }

    if (!eventData || !analysis) {
        return (
            <div style={{ 
                minHeight: '100vh', 
                background: '#0f172a',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                <div style={{ fontSize: '1.5rem', color: '#64748b' }}>No data available</div>
            </div>
        );
    }

    const currentOutcome = analysis.outcomes[selectedOutcome];

    return (
        <div style={{
            minHeight: '100vh',
            background: '#0f172a',
            color: '#e2e8f0'
        }}>
            {/* Header */}
            <div style={{
                background: '#1e293b',
                borderBottom: '1px solid #334155',
                padding: '1.5rem 2rem'
            }}>
                <div style={{ maxWidth: '1600px', margin: '0 auto' }}>
                    <Link to="/" style={{
                        color: '#94a3b8',
                        textDecoration: 'none',
                        fontSize: '0.875rem',
                        display: 'inline-block',
                        marginBottom: '0.75rem',
                        transition: 'color 0.2s'
                    }}>
                        ← Back to Markets
                    </Link>
                    <h1 style={{
                        fontSize: '1.75rem',
                        fontWeight: '700',
                        color: '#f1f5f9',
                        marginBottom: '0.5rem',
                        lineHeight: '1.3'
                    }}>
                        {eventData.title}
                    </h1>
                    {eventData.description && (
                        <p style={{ 
                            color: '#94a3b8', 
                            fontSize: '0.875rem', 
                            lineHeight: '1.5',
                            maxWidth: '900px',
                            margin: '0 auto',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical'
                        }}>
                            {eventData.description}
                        </p>
                    )}
                </div>
            </div>

            {/* Main Content */}
            <div style={{ maxWidth: '1600px', margin: '0 auto', padding: '2rem' }}>
                {/* Outcome Selector */}
                <div style={{
                    display: 'flex',
                    gap: '0.75rem',
                    marginBottom: '2rem',
                    overflowX: 'auto',
                    paddingBottom: '0.5rem'
                }}>
                    {analysis.outcomes.map((outcome, idx) => (
                        <button
                            key={idx}
                            onClick={() => setSelectedOutcome(idx)}
                            style={{
                                background: selectedOutcome === idx ? '#6366f1' : '#1e293b',
                                color: selectedOutcome === idx ? 'white' : '#94a3b8',
                                border: selectedOutcome === idx ? '1px solid #6366f1' : '1px solid #334155',
                                padding: '0.75rem 1.5rem',
                                borderRadius: '8px',
                                fontSize: '0.875rem',
                                fontWeight: '600',
                                cursor: 'pointer',
                                transition: 'all 0.2s',
                                whiteSpace: 'nowrap'
                            }}
                        >
                            {outcome.outcome_name}
                            <span style={{ 
                                marginLeft: '0.5rem', 
                                opacity: 0.7,
                                fontSize: '0.75rem'
                            }}>
                                {outcome.current_price.toFixed(1)}¢
                            </span>
                        </button>
                    ))}
                </div>

                {/* Three Column Layout */}
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: '350px 1fr 350px',
                    gap: '1.5rem',
                    marginBottom: '2rem'
                }}>
                    {/* Left: News Articles */}
                    <div style={{
                        background: '#1e293b',
                        borderRadius: '12px',
                        border: '1px solid #334155',
                        padding: '1.5rem',
                        maxHeight: '800px',
                        overflowY: 'auto'
                    }}>
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            marginBottom: '1rem'
                        }}>
                            <span style={{ fontSize: '1.25rem' }}>📰</span>
                            <h3 style={{
                                fontSize: '1rem',
                                fontWeight: '700',
                                color: '#f1f5f9',
                                margin: 0
                            }}>
                                News Sentiment
                            </h3>
                        </div>

                        {/* News Score */}
                        <div style={{
                            background: '#0f172a',
                            borderRadius: '8px',
                            padding: '1rem',
                            marginBottom: '1rem',
                            border: '1px solid #334155'
                        }}>
                            <div style={{
                                fontSize: '2.5rem',
                                fontWeight: '800',
                                color: getSentimentColor(currentOutcome.news.score),
                                marginBottom: '0.5rem'
                            }}>
                                {currentOutcome.news.score > 0 ? '+' : ''}{currentOutcome.news.score}
                            </div>
                            <div style={{
                                fontSize: '0.75rem',
                                color: '#64748b',
                                marginBottom: '0.75rem'
                            }}>
                                {currentOutcome.news.articles_count} articles (last 7 days)
                            </div>
                            <div style={{
                                fontSize: '0.875rem',
                                color: '#94a3b8',
                                lineHeight: '1.5'
                            }}>
                                {currentOutcome.news.reasoning}
                            </div>
                        </div>

                        {/* Query Info */}
                        {currentOutcome.news.query_used && (
                            <div style={{
                                fontSize: '0.75rem',
                                color: '#64748b',
                                padding: '0.75rem',
                                background: '#0f172a',
                                borderRadius: '6px',
                                border: '1px solid #334155',
                                fontFamily: 'monospace',
                                marginBottom: '1rem'
                            }}>
                                Query: {currentOutcome.news.query_used}
                            </div>
                        )}

                        {/* News Articles List */}
                        {currentOutcome.news.articles && currentOutcome.news.articles.length > 0 && (
                            <div style={{ marginTop: '1rem' }}>
                                <div style={{
                                    fontSize: '0.75rem',
                                    color: '#64748b',
                                    marginBottom: '0.75rem',
                                    textTransform: 'uppercase',
                                    letterSpacing: '0.5px',
                                    fontWeight: '600'
                                }}>
                                    Recent Articles
                                </div>
                                {currentOutcome.news.articles.slice(0, 5).map((article, idx) => (
                                    <a
                                        key={idx}
                                        href={article.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        style={{
                                            display: 'block',
                                            background: '#0f172a',
                                            border: '1px solid #334155',
                                            borderRadius: '6px',
                                            padding: '0.75rem',
                                            marginBottom: '0.5rem',
                                            textDecoration: 'none',
                                            transition: 'all 0.2s'
                                        }}
                                        onMouseEnter={(e) => {
                                            e.currentTarget.style.borderColor = '#6366f1';
                                            e.currentTarget.style.background = '#1e293b';
                                        }}
                                        onMouseLeave={(e) => {
                                            e.currentTarget.style.borderColor = '#334155';
                                            e.currentTarget.style.background = '#0f172a';
                                        }}
                                    >
                                        <div style={{
                                            fontSize: '0.875rem',
                                            color: '#f1f5f9',
                                            marginBottom: '0.25rem',
                                            fontWeight: '600',
                                            lineHeight: '1.4'
                                        }}>
                                            {article.title}
                                        </div>
                                        <div style={{
                                            fontSize: '0.75rem',
                                            color: '#64748b'
                                        }}>
                                            {article.source} • {new Date(article.publishedAt).toLocaleDateString()}
                                        </div>
                                    </a>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Center: Polymarket Embed */}
                    <div style={{
                        background: '#1e293b',
                        borderRadius: '12px',
                        border: '1px solid #334155',
                        padding: '1.5rem',
                        display: 'flex',
                        flexDirection: 'column'
                    }}>
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            marginBottom: '1rem'
                        }}>
                            <span style={{ fontSize: '1.25rem' }}>📊</span>
                            <h3 style={{
                                fontSize: '1rem',
                                fontWeight: '700',
                                color: '#f1f5f9',
                                margin: 0
                            }}>
                                Live Market
                            </h3>
                        </div>

                        {/* Polymarket Link */}
                        <div style={{
                            flex: 1,
                            background: '#0f172a',
                            borderRadius: '8px',
                            border: '1px solid #334155',
                            padding: '2rem',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            minHeight: '600px'
                        }}>
                            <div style={{
                                fontSize: '3rem',
                                marginBottom: '1rem'
                            }}>📊</div>
                            <h3 style={{
                                fontSize: '1.25rem',
                                fontWeight: '700',
                                color: '#f1f5f9',
                                marginBottom: '0.5rem'
                            }}>
                                View on Polymarket
                            </h3>
                            <p style={{
                                color: '#94a3b8',
                                marginBottom: '1.5rem',
                                textAlign: 'center',
                                maxWidth: '400px'
                            }}>
                                Trade this market, view full order book, and see detailed charts on Polymarket
                            </p>
                            <a
                                href={`https://polymarket.com/event/${eventId}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{
                                    background: '#6366f1',
                                    color: 'white',
                                    padding: '0.75rem 2rem',
                                    borderRadius: '8px',
                                    textDecoration: 'none',
                                    fontWeight: '600',
                                    fontSize: '0.95rem',
                                    transition: 'all 0.2s',
                                    display: 'inline-block'
                                }}
                            >
                                Open in Polymarket →
                            </a>
                        </div>
                    </div>

                    {/* Right: Liquidity Panel */}
                    <div style={{
                        background: '#1e293b',
                        borderRadius: '12px',
                        border: '1px solid #334155',
                        padding: '1.5rem',
                        maxHeight: '800px',
                        overflowY: 'auto'
                    }}>
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            marginBottom: '1rem'
                        }}>
                            <span style={{ fontSize: '1.25rem' }}>💧</span>
                            <h3 style={{
                                fontSize: '1rem',
                                fontWeight: '700',
                                color: '#f1f5f9',
                                margin: 0
                            }}>
                                Liquidity Score
                            </h3>
                        </div>

                        {/* Liquidity Score */}
                        <div style={{
                            background: '#0f172a',
                            borderRadius: '8px',
                            padding: '1.5rem',
                            marginBottom: '1rem',
                            border: '1px solid #334155',
                            textAlign: 'center'
                        }}>
                            <div style={{
                                fontSize: '3.5rem',
                                fontWeight: '800',
                                color: getScoreColor(currentOutcome.liquidity.score),
                                marginBottom: '0.5rem',
                                lineHeight: '1'
                            }}>
                                {currentOutcome.liquidity.score}
                            </div>
                            <div style={{
                                fontSize: '0.875rem',
                                color: '#64748b',
                                marginBottom: '1rem'
                            }}>
                                out of 100
                            </div>
                            <div style={{
                                display: 'inline-block',
                                padding: '0.5rem 1rem',
                                background: getScoreColor(currentOutcome.liquidity.score) + '20',
                                color: getScoreColor(currentOutcome.liquidity.score),
                                borderRadius: '6px',
                                fontSize: '0.875rem',
                                fontWeight: '700',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px'
                            }}>
                                {currentOutcome.liquidity.level}
                            </div>
                        </div>

                        {/* Liquidity Details */}
                        <div style={{
                            background: '#0f172a',
                            borderRadius: '8px',
                            padding: '1rem',
                            border: '1px solid #334155'
                        }}>
                            <div style={{
                                fontSize: '0.75rem',
                                color: '#64748b',
                                marginBottom: '0.5rem',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px',
                                fontWeight: '600'
                            }}>
                                Total Liquidity
                            </div>
                            <div style={{
                                fontSize: '1.5rem',
                                fontWeight: '700',
                                color: '#f1f5f9',
                                marginBottom: '1rem'
                            }}>
                                ${currentOutcome.liquidity.amount.toLocaleString()}
                            </div>
                            <div style={{
                                fontSize: '0.875rem',
                                color: '#94a3b8',
                                lineHeight: '1.6'
                            }}>
                                {currentOutcome.liquidity.reasoning}
                            </div>
                        </div>

                        {/* All Outcomes Liquidity */}
                        <div style={{ marginTop: '1.5rem' }}>
                            <div style={{
                                fontSize: '0.75rem',
                                color: '#64748b',
                                marginBottom: '0.75rem',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px',
                                fontWeight: '600'
                            }}>
                                All Outcomes
                            </div>
                            {analysis.outcomes.map((outcome, idx) => (
                                <div
                                    key={idx}
                                    style={{
                                        background: '#0f172a',
                                        border: '1px solid #334155',
                                        borderRadius: '6px',
                                        padding: '0.75rem',
                                        marginBottom: '0.5rem',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s',
                                        opacity: selectedOutcome === idx ? 1 : 0.6
                                    }}
                                    onClick={() => setSelectedOutcome(idx)}
                                >
                                    <div style={{
                                        fontSize: '0.75rem',
                                        color: '#94a3b8',
                                        marginBottom: '0.25rem'
                                    }}>
                                        {outcome.outcome_name}
                                    </div>
                                    <div style={{
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'center'
                                    }}>
                                        <div style={{
                                            fontSize: '0.875rem',
                                            fontWeight: '700',
                                            color: getScoreColor(outcome.liquidity.score)
                                        }}>
                                            {outcome.liquidity.score}/100
                                        </div>
                                        <div style={{
                                            fontSize: '0.75rem',
                                            color: '#64748b'
                                        }}>
                                            ${outcome.liquidity.amount.toLocaleString()}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Bottom: AI Summary */}
                <div style={{
                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                    borderRadius: '12px',
                    padding: '2.5rem',
                    boxShadow: '0 4px 24px rgba(99, 102, 241, 0.3)'
                }}>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.75rem',
                        marginBottom: '1.5rem'
                    }}>
                        <span style={{ fontSize: '1.75rem' }}>🎯</span>
                        <h3 style={{
                            fontSize: '1.5rem',
                            fontWeight: '700',
                            color: 'white',
                            margin: 0
                        }}>
                            Overall Analysis
                        </h3>
                    </div>
                    <div style={{
                        fontSize: '1.125rem',
                        lineHeight: '2',
                        color: 'white',
                        fontWeight: '500',
                        whiteSpace: 'pre-line',
                        textAlign: 'center',
                        maxWidth: '1000px',
                        margin: '0 auto'
                    }}>
                        {currentOutcome.final_summary}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AnalysisPage;
