#!/usr/bin/env python3
"""
Market Data Fetcher
Fetches stock market data using yfinance
"""

import yfinance as yf
import pandas as pd
import logging
import re
from typing import Dict, List, Tuple, Optional

class MarketDataFetcher:
    """Enhanced market data fetcher with better coverage and error handling"""
    
    def __init__(self):
        """Initialize the market data fetcher"""
        self.logger = logging.getLogger(__name__)
        
        # Common market suffixes for international stocks
        self.market_suffixes = {
            'israel': '.TA',
            'london': '.L',
            'toronto': '.TO',
            'frankfurt': '.F',
            'paris': '.PA',
            'milan': '.MI',
            'madrid': '.MC',
            'amsterdam': '.AS',
            'stockholm': '.ST',
            'oslo': '.OL',
            'copenhagen': '.CO',
            'helsinki': '.HE',
            'switzerland': '.SW',
            'hong_kong': '.HK',
            'tokyo': '.T',
            'australia': '.AX'
        }
        
        # Israeli TA125/TA35 common stocks
        self.israeli_stocks = {
            'TEVA': 'TEVA.TA',
            'ICL': 'ICL.TA', 
            'CHKP': 'CHKP.TA',
            'NICE': 'NICE.TA',
            'WEWORK': 'WE.TA',
            'BANK-HAPOALIM': 'POLI.TA',
            'BANK-LEUMI': 'LUMI.TA',
            'BEZEQ': 'BEZQ.TA',
            'ELBIT': 'ESLT.TA',
            'TOWER': 'TSEM.TA'
        }
    
    def normalize_symbol(self, symbol: str) -> str:
        """
        Normalize and validate stock symbol
        
        Args:
            symbol (str): Input stock symbol
            
        Returns:
            str: Normalized symbol
        """
        symbol = symbol.upper().strip()
        
        # Check if it's a known Israeli stock
        if symbol in self.israeli_stocks:
            return self.israeli_stocks[symbol]
        
        # If already has suffix, return as is
        if '.' in symbol:
            return symbol
            
        return symbol
    
    def get_symbol_suggestions(self, symbol: str) -> List[str]:
        """
        Get symbol suggestions for invalid symbols
        
        Args:
            symbol (str): Invalid symbol
            
        Returns:
            List[str]: List of suggested symbols
        """
        suggestions = []
        symbol_upper = symbol.upper()
        
        # Check Israeli stocks
        for name, ticker in self.israeli_stocks.items():
            if symbol_upper in name or name in symbol_upper:
                suggestions.append(f"{ticker} ({name})")
        
        # Common variations
        variations = [
            symbol,
            f"{symbol}.TA",  # Israeli
            f"{symbol}.L",   # London
            f"{symbol}.TO",  # Toronto
        ]
        
        return suggestions + [f"Try: {var}" for var in variations if var != symbol]
    
    def validate_symbol(self, symbol: str) -> Tuple[bool, str, List[str]]:
        """
        Validate a stock symbol
        
        Args:
            symbol (str): Stock symbol to validate
            
        Returns:
            Tuple[bool, str, List[str]]: (is_valid, normalized_symbol, suggestions)
        """
        normalized = self.normalize_symbol(symbol)
        
        try:
            ticker = yf.Ticker(normalized)
            info = ticker.info
            
            # Check if we got valid data
            if info and info.get('regularMarketPrice') is not None:
                return True, normalized, []
            else:
                suggestions = self.get_symbol_suggestions(symbol)
                return False, normalized, suggestions
                
        except Exception as e:
            suggestions = self.get_symbol_suggestions(symbol)
            return False, normalized, suggestions

    def get_stock_data(self, symbol, period="1mo"):
        """
        Fetch historical stock data with enhanced error handling
        
        Args:
            symbol (str): Stock ticker symbol
            period (str): Time period (1mo, 3mo, 6mo, 1y, 2y)
            
        Returns:
            pd.DataFrame: Historical stock data
        """
        # Normalize symbol first
        normalized_symbol = self.normalize_symbol(symbol)
        
        try:
            ticker = yf.Ticker(normalized_symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                self.logger.warning(f"No data found for {normalized_symbol}")
                return pd.DataFrame()
            
            # Check data quality
            if len(data) < 5:
                self.logger.warning(f"Limited data for {normalized_symbol}: only {len(data)} data points")
            
            # Standardize column names
            data.columns = [col.lower().replace(' ', '_') for col in data.columns]
            data['symbol'] = normalized_symbol
            data['daily_return'] = data['close'].pct_change()
            
            self.logger.info(f"Successfully fetched {len(data)} data points for {normalized_symbol}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching {normalized_symbol}: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self, symbol):
        """
        Fetch stock information and metrics with enhanced error handling
        
        Args:
            symbol (str): Stock ticker symbol
            
        Returns:
            dict: Stock information
        """
        normalized_symbol = self.normalize_symbol(symbol)
        
        try:
            ticker = yf.Ticker(normalized_symbol)
            info = ticker.info
            
            if not info or len(info) < 5:
                self.logger.warning(f"Limited info available for {normalized_symbol}")
                return {
                    'symbol': normalized_symbol,
                    'error': 'Limited information available',
                    'suggestions': self.get_symbol_suggestions(symbol)
                }
            
            # Extract data with fallbacks
            result = {
                'symbol': normalized_symbol,
                'company_name': info.get('longName', info.get('shortName', 'N/A')),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', info.get('enterpriseValue', 0)),
                'pe_ratio': info.get('trailingPE', info.get('forwardPE', 0)),
                'beta': info.get('beta', 0),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'N/A'),
                'country': info.get('country', 'N/A')
            }
            
            # Add data quality indicator
            quality_score = sum([
                1 for key in ['company_name', 'sector', 'market_cap', 'current_price'] 
                if result.get(key) not in [0, 'N/A', None]
            ])
            result['data_quality'] = f"{quality_score}/4"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error fetching info for {normalized_symbol}: {e}")
            return {
                'symbol': normalized_symbol, 
                'error': str(e),
                'suggestions': self.get_symbol_suggestions(symbol)
            }

if __name__ == "__main__":
    # Test the enhanced fetcher
    fetcher = MarketDataFetcher()
    
    # Test various symbols including problematic ones
    test_symbols = ['AAPL', 'TEVA', 'INVALID123', 'BANK-HAPOALIM', 'MSFT']
    
    print("🔍 ENHANCED MARKET DATA TESTING")
    print("=" * 50)
    
    for symbol in test_symbols:
        print(f"\n📊 Testing: {symbol}")
        
        # Validate symbol
        is_valid, normalized, suggestions = fetcher.validate_symbol(symbol)
        print(f"   Valid: {is_valid} | Normalized: {normalized}")
        if suggestions:
            print(f"   Suggestions: {suggestions[:3]}")
        
        # Get data
        data = fetcher.get_stock_data(symbol)
        if not data.empty:
            print(f"   Data: {len(data)} records, Latest: ${data['close'].iloc[-1]:.2f}")
        else:
            print(f"   Data: No data available")
        
        # Get info
        info = fetcher.get_stock_info(symbol)
        if 'error' not in info:
            print(f"   Info: {info.get('company_name', 'N/A')} | Quality: {info.get('data_quality', 'N/A')}")
        else:
            print(f"   Info: {info['error']}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing complete!")
