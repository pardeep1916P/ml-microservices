
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [backendStatus, setBackendStatus] = useState('checking');

  const API_URL = process.env.NODE_ENV === 'production' ? 'http://localhost:5000' : '';

  const spamExamples = [
    "FREE! Win $1000 cash prize now! Click here!",
    "Congratulations! You've won a free iPhone. Claim now!",
    "Buy cheap pills online. Best prices guaranteed!",
    "URGENT: Your account will be closed. Verify now!",
    "Make money from home. No experience needed!"
  ];

  const hamExamples = [
    "Hi, how are you? Let's meet for coffee tomorrow.",
    "The project deadline is next Friday. Please review the document.",
    "Thanks for your help with the presentation yesterday.",
    "Reminder: Team meeting at 3pm in conference room.",
    "Can you send me the latest report when you have time?"
  ];

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

  const handlePredict = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
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
        body: JSON.stringify({ text }),
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

  const loadExample = (example) => {
    setText(example);
    setResult(null);
    setError('');
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>📧 Spam Detection System</h1>
          <p className="subtitle">AI-powered email and message spam filter</p>
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
          <p><strong>How it works:</strong> Enter any text message or email content, and the AI will classify it as spam or legitimate (ham).</p>
          <p>Try the example messages below or write your own!</p>
        </div>

        <div className="examples-section">
          <div className="examples-column">
            <h3>🚫 Spam Examples</h3>
            {spamExamples.map((example, idx) => (
              <button 
                key={idx} 
                className="example-btn spam-example"
                onClick={() => loadExample(example)}
              >
                {example}
              </button>
            ))}
          </div>
          <div className="examples-column">
            <h3>✅ Ham Examples</h3>
            {hamExamples.map((example, idx) => (
              <button 
                key={idx} 
                className="example-btn ham-example"
                onClick={() => loadExample(example)}
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        <div className="input-section">
          <label htmlFor="text-input">Enter text to analyze:</label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type or paste your message here..."
            rows={6}
          />
          <div className="char-count">{text.length} characters</div>
        </div>

        <div className="button-group">
          <button className="btn-predict" onClick={handlePredict} disabled={loading || !text.trim()}>
            {loading ? '⏳ Analyzing...' : '🔍 Check for Spam'}
          </button>
          <button className="btn-clear" onClick={() => { setText(''); setResult(null); setError(''); }} disabled={loading}>
            🗑️ Clear
          </button>
        </div>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {result && (
          <div className={`result-container ${result.is_spam ? 'spam' : 'ham'}`}>
            <div className="result-header">
              <div className="result-icon">{result.is_spam ? '🚫' : '✅'}</div>
              <div>
                <div className="result-title">
                  {result.is_spam ? 'SPAM DETECTED!' : 'LEGITIMATE MESSAGE'}
                </div>
                <div className="result-subtitle">
                  {result.is_spam ? 'This message appears to be spam' : 'This message appears to be legitimate'}
                </div>
              </div>
            </div>
            <div className="result-details">
              <div className="result-item">
                <div className="result-label">Classification</div>
                <div className="result-value">{result.is_spam ? 'Spam' : 'Ham'}</div>
              </div>
              <div className="result-item">
                <div className="result-label">Confidence</div>
                <div className="result-value">{(result.confidence * 100).toFixed(1)}%</div>
              </div>
              <div className="result-item">
                <div className="result-label">Spam Probability</div>
                <div className="result-value">{(result.spam_probability * 100).toFixed(1)}%</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
