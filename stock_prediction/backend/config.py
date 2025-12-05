import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
API_MODE = os.getenv('API_MODE', 'yfinance')  # 'yfinance' or 'alphavantage'

# Model Configuration
MODEL_PATH = 'stock_model.pkl'
PREDICTION_DAYS = 1

# Stock Data Configuration
HISTORICAL_PERIOD = '2y'  # For training
CHART_PERIOD = '3mo'     # For charts
