import React from 'react';
import { useParams, Link } from 'react-router-dom';

function AnalysisPage() {
    const { eventId } = useParams();

    return (
        <div style={{ 
            padding: '2rem',
            textAlign: 'center',
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}>
            <div style={{
                background: 'rgba(255, 255, 255, 0.95)',
                borderRadius: '16px',
                padding: '3rem',
                maxWidth: '800px',
                margin: '0 auto',
                boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)'
            }}>
                <h1 style={{ color: '#2d3748', marginBottom: '1rem' }}>
                    Event Analysis
                </h1>
                <p style={{ color: '#718096', fontSize: '1.2rem', marginBottom: '2rem' }}>
                    Event ID: {eventId}
                </p>
                <p style={{ color: '#4a5568', fontSize: '1rem' }}>
                    Analysis page coming soon...
                </p>
                <Link 
                    to="/" 
                    style={{
                        display: 'inline-block',
                        marginTop: '2rem',
                        padding: '0.75rem 1.5rem',
                        background: '#667eea',
                        color: 'white',
                        textDecoration: 'none',
                        borderRadius: '8px',
                        fontWeight: '600',
                        transition: 'all 0.3s ease'
                    }}
                >
                    ← Back to Dashboard
                </Link>
            </div>
        </div>
    );
}

export default AnalysisPage;