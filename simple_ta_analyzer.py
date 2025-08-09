#!/usr/bin/env python3
"""
Simple Technical Analysis Functions
Fallback technical analysis for when the main library isn't available
"""

import pandas as pd
import numpy as np

class SimpleTechnicalAnalyzer:
    """Simple technical analysis with manual calculations"""
    
    def __init__(self):
        self.name = "Simple TA"
        print("Using simple technical analysis calculations")
    
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