# 📊 Stock Price Predictor

An AI-powered stock price prediction application using Machine Learning.

## 🚀 Features

- **Real-time Stock Data**: Uses yfinance API (no API key needed!)
- **ML Predictions**: Random Forest model trained on technical indicators
- **Beautiful UI**: Modern React frontend with charts
- **Technical Analysis**: MA, RSI, volatility, and more
- **Historical Charts**: 3-month price history visualization

## 🛠️ Setup Instructions

### Backend Setup

```bash
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Configure Alpha Vantage API
# Copy .env.example to .env and add your API key
copy .env.example .env
# Edit .env and set:
# ALPHA_VANTAGE_API_KEY=your_key_here
# API_MODE=alphavantage  (or keep as 'yfinance' for free API)

# Train the model (this will fetch stock data and train)
python train_model.py

# Run the Flask server
python app.py
```

Backend will run on `http://localhost:5000`

**Note**: By default, the app uses **yfinance** (free, no API key needed). To use Alpha Vantage:
1. Get free API key: https://www.alphavantage.co/support/#api-key
2. Create `.env` file from `.env.example`
3. Set your API key and change `API_MODE=alphavantage`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will open at `http://localhost:3000`

## 📖 How to Use

1. Make sure both backend and frontend are running
2. Enter a stock symbol (e.g., AAPL, GOOGL, MSFT, TSLA)
3. Click "Predict" to get next day's price prediction
4. View historical price chart and prediction details

## 🧠 Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: 10 technical indicators
  - Moving Averages (5, 10, 20 day)
  - Relative Strength Index (RSI)
  - Volatility
  - Price changes
  - Volume changes
  - High-Low differences
- **Training Data**: Historical data from multiple stocks
- **Data Source**: Yahoo Finance (via yfinance)

## 🔑 Stock Data APIs

This project supports **two data sources**:

### 1. **yfinance** (Default - FREE, No API Key!) ✅
- Completely free
- No registration needed
- Perfect for development and testing
- Already configured and ready to use

### 2. **Alpha Vantage** (Optional - Enhanced Data)
- **Free tier**: 25 API calls/day, up to 5 calls/minute
- **Data available**:
  - Daily historical data (20+ years)
  - Intraday data (1min, 5min, 15min, 30min, 60min intervals)
  - Company fundamentals
  - Real-time quotes
- **Get FREE API Key**: https://www.alphavantage.co/support/#api-key
- **Setup**:
  ```bash
  # Create .env file
  copy backend\.env.example backend\.env
  
  # Edit .env and set:
  ALPHA_VANTAGE_API_KEY=your_actual_key
  API_MODE=alphavantage
  ```

### Other Free Alternatives:
- **Finnhub** (60 calls/min) - https://finnhub.io
- **IEX Cloud** (100 calls/day) - https://iexcloud.io

## ⚠️ Disclaimer

This application is for **educational purposes only**. The predictions are made by a machine learning model and should NOT be used as financial advice. Always do your own research before making investment decisions.

## 🎨 Tech Stack

- **Backend**: Flask, scikit-learn, yfinance, pandas
- **Frontend**: React, Recharts, Axios
- **ML**: Random Forest Regressor

## 📝 API Endpoints

- `GET /` - Health check
- `POST /api/predict` - Get stock price prediction
  ```json
  {"symbol": "AAPL"}
  ```
- `GET /api/historical/<symbol>` - Get historical data
- `GET /api/stocks/popular` - Get popular stock symbols

## 🐛 Troubleshooting

**Backend won't start?**
- Make sure you ran `python train_model.py` first
- Check that all dependencies are installed

**Frontend shows connection error?**
- Ensure backend is running on port 5000
- Check CORS is enabled in Flask

**Model training fails?**
- Check internet connection (needs to fetch stock data)
- Try running with a single stock first

---

Made with ❤️ using React + Flask + Machine Learning
