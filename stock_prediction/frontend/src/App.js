import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

const API_URL = 'http://localhost:5000';

function App() {
  const [symbol, setSymbol] = useState('AAPL');
  const [prediction, setPrediction] = useState(null);
  const [historical, setHistorical] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [popularStocks, setPopularStocks] = useState([]);

  useEffect(() => {
    // Fetch popular stocks on mount
    axios.get(`${API_URL}/api/stocks/popular`)
      .then(res => setPopularStocks(res.data))
      .catch(err => console.error('Error fetching popular stocks:', err));
  }, []);

  const fetchPrediction = async () => {
    if (!symbol.trim()) {
      setError('Please enter a stock symbol');
      return;
    }

    setLoading(true);
    setError('');
    setPrediction(null);

    try {
      // Fetch prediction
      const predRes = await axios.post(`${API_URL}/api/predict`, { symbol: symbol.toUpperCase() });
      setPrediction(predRes.data);

      // Fetch historical data
      const histRes = await axios.get(`${API_URL}/api/historical/${symbol.toUpperCase()}?period=3mo`);
      setHistorical(histRes.data.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch data. Make sure the backend is running.');
      setPrediction(null);
      setHistorical([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchPrediction();
  };

  const selectStock = (stockSymbol) => {
    setSymbol(stockSymbol);
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <div className="header-content">
            <h1 className="title">
              <span className="emoji">📈</span>
              Stock Price Predictor
            </h1>
            <p className="subtitle">AI-Powered Machine Learning Predictions</p>
          </div>
        </header>

        <div className="content">
          {/* Search Section */}
          <div className="card search-card">
            <form onSubmit={handleSubmit} className="search-form">
              <div className="input-group">
                <input
                  type="text"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                  placeholder="Enter stock symbol (e.g., AAPL)"
                  className="stock-input"
                />
                <button type="submit" disabled={loading} className="predict-btn">
                  {loading ? '⏳ Analyzing...' : '🔮 Predict'}
                </button>
              </div>
            </form>

            {/* Popular Stocks */}
            <div className="popular-stocks">
              <p className="popular-label">Popular:</p>
              <div className="stock-chips">
                {popularStocks.slice(0, 5).map(stock => (
                  <button
                    key={stock.symbol}
                    onClick={() => selectStock(stock.symbol)}
                    className={`stock-chip ${symbol === stock.symbol ? 'active' : ''}`}
                  >
                    {stock.symbol}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="card error-card">
              <p className="error-text">⚠️ {error}</p>
            </div>
          )}

          {/* Prediction Result */}
          {prediction && (
            <div className="card prediction-card">
              <div className="prediction-header">
                <h2>{prediction.company_name}</h2>
                <span className="symbol-badge">{prediction.symbol}</span>
              </div>
              
              <div className="prediction-grid">
                <div className="prediction-item">
                  <span className="label">Current Price</span>
                  <span className="value current">${prediction.current_price}</span>
                  <span className="date">as of {prediction.last_updated}</span>
                </div>
                
                <div className="prediction-item">
                  <span className="label">Predicted Price</span>
                  <span className="value predicted">${prediction.predicted_price}</span>
                  <span className="date">{prediction.prediction_date}</span>
                </div>
                
                <div className="prediction-item">
                  <span className="label">Expected Change</span>
                  <span className={`value change ${prediction.percent_change >= 0 ? 'positive' : 'negative'}`}>
                    {prediction.percent_change >= 0 ? '↑' : '↓'} {Math.abs(prediction.percent_change).toFixed(2)}%
                  </span>
                  <span className="date">${prediction.price_change >= 0 ? '+' : ''}{prediction.price_change.toFixed(2)}</span>
                </div>
              </div>

              {prediction.percent_change >= 0 ? (
                <div className="prediction-message success">
                  <span>📊 Model predicts an upward trend</span>
                </div>
              ) : (
                <div className="prediction-message warning">
                  <span>📉 Model predicts a downward trend</span>
                </div>
              )}
            </div>
          )}

          {/* Historical Chart */}
          {historical.length > 0 && (
            <div className="card chart-card">
              <h3 className="chart-title">3-Month Historical Price</h3>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={historical}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis 
                      dataKey="date" 
                      stroke="rgba(255,255,255,0.7)"
                      tick={{ fill: 'rgba(255,255,255,0.7)' }}
                    />
                    <YAxis 
                      stroke="rgba(255,255,255,0.7)"
                      tick={{ fill: 'rgba(255,255,255,0.7)' }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(0,0,0,0.8)', 
                        border: '1px solid rgba(255,255,255,0.2)',
                        borderRadius: '8px'
                      }}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="close" 
                      stroke="#4ade80" 
                      strokeWidth={2}
                      dot={false}
                      name="Close Price"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Info Card */}
          {!prediction && !loading && (
            <div className="card info-card">
              <h3>🤖 How It Works</h3>
              <ul className="info-list">
                <li>📊 Analyzes historical stock data using yfinance</li>
                <li>🧠 Random Forest ML model trained on multiple stocks</li>
                <li>📈 Uses technical indicators (MA, RSI, volatility)</li>
                <li>🔮 Predicts next day's closing price</li>
              </ul>
              <p className="disclaimer">
                ⚠️ <strong>Disclaimer:</strong> This is for educational purposes only. 
                Not financial advice. Always do your own research.
              </p>
            </div>
          )}
        </div>

        <footer className="footer">
          <p>Made with ❤️ using React + Flask + ML</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
