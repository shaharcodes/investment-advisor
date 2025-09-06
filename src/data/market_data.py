#!/usr/bin/env python3
"""
Market Data Fetcher
Fetches stock market data using yfinance
"""

import yfinance as yf
import pandas as pd
import logging

class MarketDataFetcher:
    """Fetches market data for stocks"""
    
    def __init__(self):
        """Initialize the market data fetcher"""
        self.logger = logging.getLogger(__name__)
    
    def get_stock_data(self, symbol, period="1mo"):
        """
        Fetch historical stock data
        
        Args:
            symbol (str): Stock ticker symbol
            period (str): Time period (1mo, 3mo, 6mo, 1y, 2y)
            
        Returns:
            pd.DataFrame: Historical stock data
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                return pd.DataFrame()
            
            # Standardize column names
            data.columns = [col.lower().replace(' ', '_') for col in data.columns]
            data['symbol'] = symbol
            data['daily_return'] = data['close'].pct_change()
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching {symbol}: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self, symbol):
        """
        Fetch stock information and metrics
        
        Args:
            symbol (str): Stock ticker symbol
            
        Returns:
            dict: Stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'beta': info.get('beta', 0),
                'current_price': info.get('currentPrice', 0)
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching info for {symbol}: {e}")
            return {'symbol': symbol, 'error': str(e)}

if __name__ == "__main__":
    # Test the fetcher
    fetcher = MarketDataFetcher()
    data = fetcher.get_stock_data('AAPL')
    print(f"AAPL data: {len(data)} records")
    
    if not data.empty:
        print(f"Latest price: ${data['close'].iloc[-1]:.2f}")
        
    info = fetcher.get_stock_info('AAPL')
    print(f"Company: {info.get('company_name', 'N/A')}")
