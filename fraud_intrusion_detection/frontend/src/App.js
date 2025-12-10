
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [features, setFeatures] = useState(Array(10).fill(''));
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [backendStatus, setBackendStatus] = useState('checking');

  // Use proxy in development, direct URL in production
  const API_URL = process.env.NODE_ENV === 'production' ? 'http://localhost:5000' : '';

  useEffect(() => {
    checkBackendStatus();
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

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    setFeatures(newFeatures);
  };

  const fillRandom = () => {
    const randomFeatures = Array(10).fill(0).map(() => 
      (Math.random() * 6 - 3).toFixed(2)
    );
    setFeatures(randomFeatures);
  };

  const clearInputs = () => {
    setFeatures(Array(10).fill(''));
    setResult(null);
    setError('');
  };

  const handlePredict = async () => {
    const featureValues = features.map(f => parseFloat(f));
    
    if (featureValues.some(isNaN)) {
      setError('Please fill in all 10 features with valid numbers');
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
        body: JSON.stringify({ features: featureValues }),
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

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🛡️ Fraud & Intrusion Detection System</h1>
          <p className="subtitle">AI-powered security analysis using machine learning</p>
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
          <p><strong>How it works:</strong> This system analyzes 10 different features to detect potential fraud or intrusion attempts.</p>
          <p>Enter feature values (typically normalized between -3 and 3) or use random values to test the model.</p>
        </div>

        <div className="feature-grid">
          {features.map((value, index) => (
            <div key={index} className="feature-input">
              <label htmlFor={`feature-${index}`}>Feature {index + 1}</label>
              <input
                id={`feature-${index}`}
                type="number"
                step="0.1"
                value={value}
                onChange={(e) => handleFeatureChange(index, e.target.value)}
                placeholder="0.0"
              />
            </div>
          ))}
        </div>

        <div className="button-group">
          <button className="btn-predict" onClick={handlePredict} disabled={loading}>
            {loading ? '⏳ Analyzing...' : '🔍 Analyze'}
          </button>
          <button className="btn-random" onClick={fillRandom} disabled={loading}>
            🎲 Random Values
          </button>
          <button className="btn-clear" onClick={clearInputs} disabled={loading}>
            🗑️ Clear
          </button>
        </div>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {result && (
          <div className={`result-container ${result.is_fraud ? 'fraud' : 'safe'}`}>
            <div className="result-header">
              <div className="result-icon">{result.is_fraud ? '⚠️' : '✅'}</div>
              <div>
                <div className="result-title">
                  {result.is_fraud ? 'FRAUD DETECTED!' : 'SAFE - No Fraud Detected'}
                </div>
              </div>
            </div>
            <div className="result-details">
              <div className="result-item">
                <div className="result-label">Prediction</div>
                <div className="result-value">{result.is_fraud ? 'Fraud' : 'Normal'}</div>
              </div>
              <div className="result-item">
                <div className="result-label">Confidence</div>
                <div className="result-value">{(result.confidence * 100).toFixed(1)}%</div>
              </div>
              <div className="result-item">
                <div className="result-label">Risk Score</div>
                <div className="result-value">{(result.risk_score * 100).toFixed(1)}%</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
