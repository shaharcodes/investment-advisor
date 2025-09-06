#!/usr/bin/env python3
"""
FALLBACK: Simple Technical Analysis Calculator
Manual implementation of core technical indicators as backup for when main 'ta' library isn't available
Used as abstraction layer and dependency insurance
"""

import pandas as pd
import numpy as np

class SimpleTechnicalAnalyzer:
    """Simple technical analysis with manual calculations"""
    
    def __init__(self):
        self.name = "Simple TA (Fallback)"
        print("Using fallback technical analysis calculations")
    
    def rsi(self, data: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
        """Calculate RSI manually"""
        delta = data[column].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.ewm(com=period-1, adjust=False).mean()
        avg_loss = loss.ewm(com=period-1, adjust=False).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def sma(self, data: pd.DataFrame, period: int = 20, column: str = 'close') -> pd.Series:
        """Calculate Simple Moving Average"""
        return data[column].rolling(window=period).mean()
    
    def ema(self, data: pd.DataFrame, period: int = 20, column: str = 'close') -> pd.Series:
        """Calculate Exponential Moving Average"""
        return data[column].ewm(span=period, adjust=False).mean()
    
    def macd(self, data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9, column: str = 'close') -> pd.DataFrame:
        """Calculate MACD"""
        exp1 = data[column].ewm(span=fast, adjust=False).mean()
        exp2 = data[column].ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return pd.DataFrame({
            'macd': macd,
            'signal': signal_line, 
            'histogram': histogram
        })
    
    def bollinger_bands(self, data: pd.DataFrame, period: int = 20, std_dev: int = 2, column: str = 'close') -> pd.DataFrame:
        """Calculate Bollinger Bands"""
        sma = self.sma(data, period, column)
        std = data[column].rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return pd.DataFrame({
            'bb_upper': upper_band,
            'bb_middle': sma,
            'bb_lower': lower_band
        })

# Test function
if __name__ == "__main__":
    print("🧪 Testing Fallback TA Calculator...")
    
    # Create sample data
    dates = pd.date_range('2024-01-01', periods=50, freq='D')
    sample_data = pd.DataFrame({
        'close': np.random.randn(50).cumsum() + 100
    }, index=dates)
    
    analyzer = SimpleTechnicalAnalyzer()
    
    # Test calculations
    rsi = analyzer.rsi(sample_data)
    sma = analyzer.sma(sample_data, 20)
    macd_data = analyzer.macd(sample_data)
    bb_data = analyzer.bollinger_bands(sample_data)
    
    print(f"✅ RSI calculated: {len(rsi.dropna())} values")
    print(f"✅ SMA calculated: {len(sma.dropna())} values") 
    print(f"✅ MACD calculated: {len(macd_data.dropna())} values")
    print(f"✅ Bollinger Bands calculated: {len(bb_data.dropna())} values")
    print("🎉 Fallback TA Calculator working properly!")
