from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from alpha_vantage_api import get_stock_history, AlphaVantageAPI
import yfinance as yf
import config

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "stock_model.pkl")
model_data = None

def load_model():
    """Load the trained model and scalers"""
    global model_data
    if model_data is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model_data = pickle.load(f)
        else:
            raise FileNotFoundError("Model not found. Please run train_model.py first")
    return model_data

def engineer_features(df):
    """Create technical indicators - same as in training"""
    df = df.copy()
    
    # Price-based features
    df['Price_Change'] = df['Close'].pct_change()
    df['High_Low_Diff'] = df['High'] - df['Low']
    df['Open_Close_Diff'] = df['Close'] - df['Open']
    
    # Moving averages
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_10'] = df['Close'].rolling(window=10).mean()
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    
    # Volatility
    df['Volatility'] = df['Close'].rolling(window=10).std()
    
    # Volume features
    df['Volume_Change'] = df['Volume'].pct_change()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df = df.dropna()
    return df

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"status": "ok", "project": "stock_prediction"})

@app.route("/api/predict", methods=["POST"])
def predict():
    """Predict next day's stock price"""
    try:
        data = request.get_json() or {}
        symbol = data.get("symbol", "AAPL").upper()
        
        # Fetch recent stock data using configured API
        df = get_stock_history(symbol, period="3mo")
        
        if df.empty:
            return jsonify({"error": f"Could not fetch data for {symbol}"}), 400
        
        # Engineer features
        df = engineer_features(df)
        
        if df.empty:
            return jsonify({"error": "Not enough data to make prediction"}), 400
        
        # Load model
        model_data = load_model()
        model = model_data['model']
        scaler_X = model_data['scaler_X']
        scaler_y = model_data['scaler_y']
        feature_cols = model_data['feature_cols']
        
        # Get latest features
        latest_features = df[feature_cols].iloc[-1].values.reshape(1, -1)
        
        # Scale features
        latest_scaled = scaler_X.transform(latest_features)
        
        # Make prediction
        pred_scaled = model.predict(latest_scaled)[0]
        
        # Inverse transform to get actual price
        prediction = scaler_y.inverse_transform([[pred_scaled]])[0][0]
        
        # Get current price and calculate change
        current_price = float(df['Close'].iloc[-1])
        price_change = prediction - current_price
        percent_change = (price_change / current_price) * 100
        
        # Get company info
        try:
            if config.API_MODE == 'alphavantage':
                av_api = AlphaVantageAPI()
                overview = av_api.get_company_overview(symbol)
                company_name = overview.get('Name', symbol)
            else:
                stock = yf.Ticker(symbol)
                info = stock.info
                company_name = info.get('longName', symbol)
        except:
            company_name = symbol
        
        return jsonify({
            "symbol": symbol,
            "company_name": company_name,
            "current_price": round(current_price, 2),
            "predicted_price": round(prediction, 2),
            "price_change": round(price_change, 2),
            "percent_change": round(percent_change, 2),
            "prediction_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "last_updated": df.index[-1].strftime("%Y-%m-%d")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/historical/<symbol>", methods=["GET"])
def get_historical(symbol):
    """Get historical stock data for charting"""
    try:
        period = request.args.get('period', '1mo')
        
        df = get_stock_history(symbol.upper(), period=period)
        
        if df.empty:
            return jsonify({"error": f"Could not fetch data for {symbol}"}), 400
        
        # Format data for frontend
        data = []
        for date, row in df.iterrows():
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "close": round(float(row['Close']), 2),
                "open": round(float(row['Open']), 2),
                "high": round(float(row['High']), 2),
                "low": round(float(row['Low']), 2),
                "volume": int(row['Volume'])
            })
        
        return jsonify({"symbol": symbol.upper(), "data": data})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/stocks/popular", methods=["GET"])
def get_popular_stocks():
    """Get list of popular stock symbols"""
    popular = [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "TSLA", "name": "Tesla, Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
        {"symbol": "V", "name": "Visa Inc."},
        {"symbol": "WMT", "name": "Walmart Inc."}
    ]
    return jsonify(popular)

if __name__ == "__main__":
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        print("\n⚠️  Model not found!")
        print("Please run: python train_model.py\n")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
