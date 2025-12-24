
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [userId, setUserId] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [backendStatus, setBackendStatus] = useState('checking');

  const API_URL = process.env.NODE_ENV === 'production' ? 'http://localhost:5000' : '';

  const sampleUsers = ['alice', 'bob', 'charlie', 'diana', 'eve'];

  useEffect(() => {
    checkBackendStatus();
    // eslint-disable-next-line
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/`);
      const data = await response.json();
      if (data.status === 'ok') {
        setBackendStatus('online');
      }
    } catch (err) {
      console.error('Backend connection error:', err);
      setBackendStatus('offline');
    }
  };

  const handlePredict = async () => {
    if (!userId.trim()) {
      setError('Please enter a user ID');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user: userId.trim() }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      setResult(data);
    } catch (err) {
      setError(`Error: ${err.message}. Make sure the backend is running on port 5000.`);
    } finally {
      setLoading(false);
    }
  };

  const loadSampleUser = (user) => {
    setUserId(user);
    setResult(null);
    setError('');
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🎯 Recommendation System</h1>
          <p className="subtitle">AI-powered personalized recommendations</p>
        </header>

        <div className={`status-indicator ${backendStatus}`}>
          <div className="status-dot"></div>
          <span>
            {backendStatus === 'online' ? 'Backend connected ✓' : 
             backendStatus === 'offline' ? 'Backend offline - Please start the backend server' : 
             'Checking backend connection...'}
          </span>
        </div>

        <div className="info-box">
          <p><strong>How it works:</strong> Enter a user ID to get personalized product recommendations based on their preferences.</p>
          <p>Try one of the sample users below or enter your own user ID!</p>
        </div>

        <div className="sample-users">
          <h3>Sample Users:</h3>
          <div className="user-buttons">
            {sampleUsers.map((user) => (
              <button
                key={user}
                className="user-btn"
                onClick={() => loadSampleUser(user)}
              >
                👤 {user}
              </button>
            ))}
          </div>
        </div>

        <div className="input-section">
          <label htmlFor="user-input">User ID:</label>
          <input
            id="user-input"
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter user ID (e.g., alice, bob)"
            onKeyPress={(e) => e.key === 'Enter' && handlePredict()}
          />
        </div>

        <div className="button-group">
          <button className="btn-predict" onClick={handlePredict} disabled={loading || !userId.trim()}>
            {loading ? '⏳ Loading...' : '🔍 Get Recommendations'}
          </button>
          <button className="btn-clear" onClick={() => { setUserId(''); setResult(null); setError(''); }} disabled={loading}>
            🗑️ Clear
          </button>
        </div>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {result && (
          <div className="result-container">
            <div className="result-header">
              <div className="result-icon">🎁</div>
              <div>
                <div className="result-title">
                  Recommendations for {result.user}
                </div>
                {result.message && (
                  <div className="result-subtitle">
                    {result.message}
                  </div>
                )}
                {result.total_items > 0 && (
                  <div className="result-subtitle">
                    Found {result.total_items} recommended {result.total_items === 1 ? 'item' : 'items'}
                  </div>
                )}
              </div>
            </div>
            
            {result.recommendations && result.recommendations.length > 0 ? (
              <div className="recommendations-grid">
                {result.recommendations.map((rec, idx) => (
                  <div key={idx} className="recommendation-card">
                    <div className="card-header">
                      <span className="rank">#{idx + 1}</span>
                      <div className="rating">
                        <span className="stars">{'⭐'.repeat(Math.round(rec.rating))}</span>
                        <span className="rating-value">{rec.rating.toFixed(1)}</span>
                      </div>
                    </div>
                    <div className="product-name">{rec.item}</div>
                    <div className="confidence-bar">
                      <div 
                        className="confidence-fill" 
                        style={{ width: `${(rec.rating / 5) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-results">
                <p>🔍 No recommendations available for this user.</p>
                <p>Try one of the sample users: {sampleUsers.join(', ')}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
