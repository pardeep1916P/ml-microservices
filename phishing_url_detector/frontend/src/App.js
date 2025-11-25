import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

function App() {
  const [url, setUrl] = useState("");
  const [features, setFeatures] = useState(Array(10).fill(""));
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [serverHealth, setServerHealth] = useState(null);
  const [showFeatureInput, setShowFeatureInput] = useState(false);

  // Check server health on mount
  useEffect(() => {
    checkServerHealth();
    const interval = setInterval(checkServerHealth, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const checkServerHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      setServerHealth(response.data.status === "healthy");
    } catch (err) {
      console.error("Server health check failed:", err);
      setServerHealth(false);
    }
  };

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    setFeatures(newFeatures);
  };

  // Function to extract features from URL
  const extractFeaturesFromUrl = (urlString) => {
    try {
      const url = new URL(urlString);
      const hostname = url.hostname;
      
      // Feature extraction for phishing detection
      const features = [
        // F1: Having IP address in URL (phishing indicator)
        /(\d{1,3}\.){3}\d{1,3}/.test(hostname) ? 95 : 5,
        
        // F2: Having @ symbol (phishing indicator)
        urlString.includes('@') ? 90 : 10,
        
        // F3: URL length (very long URLs are suspicious)
        Math.min(urlString.length > 75 ? 85 : urlString.length / 1.2, 100),
        
        // F4: Number of dots in domain (many = suspicious)
        Math.min((hostname.match(/\./g) || []).length * 15, 100),
        
        // F5: Presence of hyphen in domain (legitimate domains rarely have many)
        Math.min((hostname.match(/-/g) || []).length * 20, 100),
        
        // F6: Non-HTTPS protocol (phishing indicator)
        url.protocol !== 'https:' ? 85 : 15,
        
        // F7: Suspicious TLDs (.tk, .ml, .ru are risky)
        /\.(tk|ml|ga|cf|ru|xyz|top)$/.test(hostname) ? 90 : 10,
        
        // F8: Subdomain count (multiple subdomains = suspicious)
        Math.min((hostname.match(/\./g) || []).length * 25, 100),
        
        // F9: Special characters in URL path
        Math.min(((urlString.match(/[%@!&]/g) || []).length * 15), 100),
        
        // F10: Contains numbers in domain (sometimes phishing)
        /\d/.test(hostname) ? 70 : 20
      ];
      
      return features.map(f => parseFloat(f.toFixed(2)));
    } catch (err) {
      console.error("Invalid URL:", err);
      return null;
    }
  };

  const handleUrlChange = (e) => {
    const urlValue = e.target.value;
    setUrl(urlValue);
    
    // Auto-extract features when URL is valid
    if (urlValue.trim().length > 0) {
      const extractedFeatures = extractFeaturesFromUrl(urlValue);
      if (extractedFeatures) {
        setFeatures(extractedFeatures);
        setError(null);
      }
    }
  };

  const handleClear = () => {
    setUrl("");
    setFeatures(Array(10).fill(""));
    setResult(null);
    setError(null);
    setShowFeatureInput(false);
  };

  const validateFeatures = () => {
    for (let i = 0; i < features.length; i++) {
      if (features[i] === "") {
        setError(`Feature ${i + 1} is required`);
        return false;
      }
      const num = parseFloat(features[i]);
      if (isNaN(num)) {
        setError(`Feature ${i + 1} must be a number`);
        return false;
      }
    }
    return true;
  };

  const handlePredict = async () => {
    setError(null);
    setResult(null);

    if (!validateFeatures()) {
      return;
    }

    if (!serverHealth) {
      setError("Server is not available. Please ensure the backend is running.");
      return;
    }

    try {
      setLoading(true);
      const numericFeatures = features.map(f => parseFloat(f));
      
      const response = await axios.post(`${API_BASE_URL}/predict`, {
        features: numericFeatures
      });

      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error || "Prediction failed");
      }
    } catch (err) {
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.message === "Network Error") {
        setError("Cannot connect to backend server. Make sure it's running on port 5000.");
      } else {
        setError(err.message || "An error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRandomExample = () => {
    const randomFeatures = Array(10)
      .fill(0)
      .map(() => (Math.random() * 100).toFixed(2));
    setFeatures(randomFeatures);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🔍 Phishing URL Detector</h1>
        <p>Advanced ML-based Detection System v1.0</p>
        <div className={`server-status ${serverHealth ? "healthy" : "unhealthy"}`}>
          {serverHealth ? "✓ Backend Connected" : "✗ Backend Disconnected"}
        </div>
      </header>

      <main className="container">
        {/* URL Input Section */}
        <section className="url-section">
          <h2>📝 Enter URL to Analyze</h2>
          <div className="url-input-group">
            <input
              type="url"
              value={url}
              onChange={handleUrlChange}
              placeholder="https://example.com"
              className="url-input"
              disabled={loading}
            />
            <button
              onClick={() => setShowFeatureInput(!showFeatureInput)}
              className="btn btn-info"
              disabled={loading || !serverHealth}
            >
              {showFeatureInput ? "▼ Hide Features" : "▶ Edit Features"}
            </button>
          </div>
          <p className="url-hint">✨ Features will be auto-extracted from the URL. Click "Edit Features" to manually adjust them.</p>
        </section>

        {/* Features Input Section */}
        {showFeatureInput && (
          <section className="features-section">
            <h2>🔢 URL Features (10 numeric values)</h2>
            <p className="features-hint">Enter 10 numeric values representing URL characteristics (range: 0-100)</p>
            
            <div className="features-grid">
              {features.map((feature, index) => (
                <div key={index} className="feature-input-group">
                  <label htmlFor={`feature-${index}`}>
                    F{index + 1}
                  </label>
                  <input
                    id={`feature-${index}`}
                    type="number"
                    step="0.01"
                    min="0"
                    max="100"
                    value={feature}
                    onChange={(e) => handleFeatureChange(index, e.target.value)}
                    placeholder="0.0"
                    disabled={loading}
                    className="feature-input"
                  />
                </div>
              ))}
            </div>

            <div className="button-group">
              <button
                onClick={handlePredict}
                disabled={loading || !serverHealth}
                className="btn btn-primary"
              >
                {loading ? "🔄 Analyzing..." : "🚀 Predict"}
              </button>
              <button
                onClick={handleRandomExample}
                disabled={loading}
                className="btn btn-secondary"
              >
                🎲 Random Example
              </button>
              <button
                onClick={handleClear}
                disabled={loading}
                className="btn btn-outline"
              >
                ✖ Clear All
              </button>
            </div>
          </section>
        )}

        {/* Error Message */}
        {error && (
          <section className="error-section">
            <div className="error-message">
              <span>⚠️</span>
              <div>
                <strong>Error</strong>
                <p>{error}</p>
              </div>
            </div>
          </section>
        )}

        {/* Results Section */}
        {result && (
          <section className="result-section">
            <h2>✅ Analysis Result</h2>
            
            <div className="result-card">
              <div className="result-main">
                <div className={`prediction ${result.prediction === 0 ? "phishing" : "legitimate"}`}>
                  <div className="prediction-icon">
                    {result.prediction === 0 ? "🚨" : "✅"}
                  </div>
                  <div className="prediction-text">
                    <strong>{result.prediction === 0 ? "PHISHING DETECTED!" : "LEGITIMATE URL"}</strong>
                    <span className="confidence">
                      Confidence: {(result.confidence * 100).toFixed(2)}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="result-probabilities">
                <h3>📊 Probability Distribution</h3>
                
                <div className="probability-item">
                  <div className="prob-header">
                    <label>🚨 Phishing URL</label>
                    <span className="prob-value">{(result.probabilities.legitimate * 100).toFixed(2)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div
                      className="probability-fill"
                      style={{
                        width: `${result.probabilities.legitimate * 100}%`,
                        backgroundColor: "#FF6B6B"
                      }}
                    />
                  </div>
                </div>

                <div className="probability-item">
                  <div className="prob-header">
                    <label>✅ Legitimate URL</label>
                    <span className="prob-value">{(result.probabilities.phishing * 100).toFixed(2)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div
                      className="probability-fill"
                      style={{
                        width: `${result.probabilities.phishing * 100}%`,
                        backgroundColor: "#4CAF50"
                      }}
                    />
                  </div>
                </div>
              </div>

              <button
                onClick={handleClear}
                className="btn btn-outline"
              >
                🔄 Analyze Another URL
              </button>
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        <p>Phishing URL Detector v1.0.0 | ML-Powered Security</p>
        <p>Backend: {serverHealth ? "🟢 Running" : "🔴 Offline"}</p>
      </footer>
    </div>
  );
}

export default App;
