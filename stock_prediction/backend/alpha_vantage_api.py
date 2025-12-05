import requests
import pandas as pd
from datetime import datetime
import config

class AlphaVantageAPI:
    """Wrapper for Alpha Vantage API"""
    
    BASE_URL = 'https://www.alphavantage.co/query'
    
    def __init__(self, api_key=None):
        self.api_key = api_key or config.ALPHA_VANTAGE_API_KEY
        
    def get_daily_data(self, symbol, outputsize='full'):
        """
        Get daily time series data
        outputsize: 'compact' (100 days) or 'full' (20+ years)
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.api_key,
            'outputsize': outputsize
        }
        
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        
        if 'Error Message' in data:
            raise ValueError(f"Invalid symbol: {symbol}")
        
        if 'Note' in data:
            raise ValueError("API call frequency limit reached. Using demo key or need to upgrade.")
        
        time_series = data.get('Time Series (Daily)', {})
        
        if not time_series:
            raise ValueError(f"No data returned for {symbol}")
        
        # Convert to pandas DataFrame
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        # Rename columns
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])
        
        return df
    
    def get_intraday_data(self, symbol, interval='5min', outputsize='compact', month=None):
        """
        Get intraday time series data
        interval: 1min, 5min, 15min, 30min, 60min
        outputsize: 'compact' (100 bars) or 'full' (30 days)
        month: Optional, format '2009-01' for historical month
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'apikey': self.api_key,
            'outputsize': outputsize
        }
        
        if month:
            params['month'] = month
        
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        
        if 'Error Message' in data:
            raise ValueError(f"Invalid symbol: {symbol}")
        
        if 'Note' in data:
            raise ValueError("API call frequency limit reached.")
        
        time_series_key = f'Time Series ({interval})'
        time_series = data.get(time_series_key, {})
        
        if not time_series:
            raise ValueError(f"No data returned for {symbol}")
        
        # Convert to pandas DataFrame
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        # Rename columns
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])
        
        return df
    
    def get_company_overview(self, symbol):
        """Get company overview and fundamental data"""
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        
        return data

# Helper function to get stock data (Alpha Vantage or yfinance)
def get_stock_history(symbol, period='2y', api_mode=None):
    """
    Unified function to get stock data from either Alpha Vantage or yfinance
    """
    api_mode = api_mode or config.API_MODE
    
    if api_mode == 'alphavantage':
        try:
            av_api = AlphaVantageAPI()
            df = av_api.get_daily_data(symbol, outputsize='full')
            
            # Filter by period if needed
            if period:
                from datetime import datetime, timedelta
                period_map = {
                    '1mo': 30, '3mo': 90, '6mo': 180,
                    '1y': 365, '2y': 730, '5y': 1825
                }
                days = period_map.get(period, 730)
                cutoff_date = datetime.now() - timedelta(days=days)
                df = df[df.index >= cutoff_date]
            
            return df
        except Exception as e:
            print(f"Alpha Vantage error: {e}. Falling back to yfinance...")
            api_mode = 'yfinance'
    
    # Default to yfinance
    if api_mode == 'yfinance':
        import yfinance as yf
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df
    
    raise ValueError(f"Unknown API mode: {api_mode}")
