#!/usr/bin/env python3
"""
Train a stock prediction model using historical data
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import pickle
import os
from alpha_vantage_api import get_stock_history
import config

def fetch_stock_data(symbol='AAPL', period='2y'):
    """Fetch historical stock data using configured API"""
    print(f"Fetching data for {symbol} using {config.API_MODE}...")
    df = get_stock_history(symbol, period=period)
    return df

def engineer_features(df):
    """Create technical indicators and features"""
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
    
    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Drop NaN values
    df = df.dropna()
    
    return df

def prepare_data(df, lookback=10):
    """Prepare data for training"""
    # Features to use for prediction
    feature_cols = ['Close', 'Volume', 'High_Low_Diff', 'Open_Close_Diff',
                    'MA_5', 'MA_10', 'MA_20', 'Volatility', 'Volume_Change', 'RSI']
    
    # Target is next day's closing price
    df['Target'] = df['Close'].shift(-1)
    df = df.dropna()
    
    X = df[feature_cols].values
    y = df['Target'].values
    
    # Split data
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Scale features
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()
    
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)
    
    y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()
    y_test_scaled = scaler_y.transform(y_test.reshape(-1, 1)).ravel()
    
    return X_train_scaled, X_test_scaled, y_train_scaled, y_test_scaled, scaler_X, scaler_y, feature_cols

def train_model(X_train, y_train):
    """Train a Random Forest model"""
    print("Training model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model

def main():
    """Main training pipeline"""
    # Fetch data for multiple stocks to make model more robust
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    
    all_X_train = []
    all_y_train = []
    
    for symbol in symbols:
        try:
            print(f"\n--- Processing {symbol} ---")
            df = fetch_stock_data(symbol, period='2y')
            df = engineer_features(df)
            
            X_train, X_test, y_train, y_test, scaler_X, scaler_y, feature_cols = prepare_data(df)
            
            all_X_train.append(X_train)
            all_y_train.append(y_train)
            
            # Print some stats
            print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
            
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue
    
    # Combine all training data
    X_train_combined = np.vstack(all_X_train)
    y_train_combined = np.concatenate(all_y_train)
    
    print(f"\n--- Training on combined data ---")
    print(f"Total training samples: {len(X_train_combined)}")
    
    # Train model
    model = train_model(X_train_combined, y_train_combined)
    
    # Evaluate on test set (using last stock's test data)
    from sklearn.metrics import mean_squared_error, r2_score
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"MSE: {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")
    
    # Save model and scalers
    model_data = {
        'model': model,
        'scaler_X': scaler_X,
        'scaler_y': scaler_y,
        'feature_cols': feature_cols
    }
    
    with open('stock_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("\n✓ Model saved to stock_model.pkl")

if __name__ == '__main__':
    main()
