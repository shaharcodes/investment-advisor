#!/usr/bin/env python3
"""
Technical Analysis Engine
Comprehensive technical indicators and analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

# Try to import ta library
try:
    import ta
    HAS_TA = True
    print("✅ Using 'ta' library for technical analysis")
except ImportError:
    HAS_TA = False
    print("⚠️ 'ta' library not available, using manual calculations")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """
    Comprehensive technical analysis with multiple indicators
    """
    
    def __init__(self):
        """Initialize the technical analyzer"""
        self.has_ta_lib = HAS_TA
        logger.info(f"Technical Analyzer initialized (ta library: {HAS_TA})")
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            data: DataFrame with price data
            period: RSI period (default 14)
            column: Column to calculate RSI on
            
        Returns:
            Series with RSI values
        """
        if self.has_ta_lib:
            return ta.momentum.RSIIndicator(data[column], window=period).rsi()
        else:
            # Manual calculation
            delta = data[column].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.ewm(com=period-1, adjust=False).mean()
            avg_loss = loss.ewm(com=period-1, adjust=False).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
    
    def calculate_macd(self, data: pd.DataFrame, fast: int = 12, slow: int = 26, 
                      signal: int = 9, column: str = 'close') -> pd.DataFrame:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            data: DataFrame with price data
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line EMA period
            column: Column to calculate MACD on
            
        Returns:
            DataFrame with MACD, Signal, and Histogram
        """
        if self.has_ta_lib:
            macd_indicator = ta.trend.MACD(data[column], window_fast=fast, window_slow=slow, window_sign=signal)
            return pd.DataFrame({
                'macd': macd_indicator.macd(),
                'signal': macd_indicator.macd_signal(),
                'histogram': macd_indicator.macd_diff()
            })
        else:
            # Manual calculation
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
    
    def calculate_moving_averages(self, data: pd.DataFrame, periods: List[int] = [20, 50, 200], 
                                 column: str = 'close') -> pd.DataFrame:
        """
        Calculate multiple moving averages
        
        Args:
            data: DataFrame with price data
            periods: List of periods for moving averages
            column: Column to calculate MAs on
            
        Returns:
            DataFrame with moving averages
        """
        ma_data = pd.DataFrame(index=data.index)
        
        for period in periods:
            if self.has_ta_lib:
                ma_data[f'sma_{period}'] = ta.trend.SMAIndicator(data[column], window=period).sma_indicator()
                ma_data[f'ema_{period}'] = ta.trend.EMAIndicator(data[column], window=period).ema_indicator()
            else:
                ma_data[f'sma_{period}'] = data[column].rolling(window=period).mean()
                ma_data[f'ema_{period}'] = data[column].ewm(span=period, adjust=False).mean()
                
        return ma_data
    
    def calculate_bollinger_bands(self, data: pd.DataFrame, window: int = 20, 
                                 window_dev: int = 2, column: str = 'close') -> pd.DataFrame:
        """
        Calculate Bollinger Bands
        
        Args:
            data: DataFrame with price data
            window: Moving average window
            window_dev: Standard deviation multiplier
            column: Column to calculate bands on
            
        Returns:
            DataFrame with upper, middle, and lower bands
        """
        if self.has_ta_lib:
            bb_indicator = ta.volatility.BollingerBands(data[column], window=window, window_dev=window_dev)
            return pd.DataFrame({
                'bb_upper': bb_indicator.bollinger_hband(),
                'bb_middle': bb_indicator.bollinger_mavg(),
                'bb_lower': bb_indicator.bollinger_lband()
            })
        else:
            # Manual calculation
            sma = data[column].rolling(window=window).mean()
            std = data[column].rolling(window=window).std()
            return pd.DataFrame({
                'bb_upper': sma + (std * window_dev),
                'bb_middle': sma,
                'bb_lower': sma - (std * window_dev)
            })
    
    def calculate_stochastic(self, data: pd.DataFrame, k_period: int = 14, 
                           d_period: int = 3) -> pd.DataFrame:
        """
        Calculate Stochastic Oscillator
        
        Args:
            data: DataFrame with OHLC data
            k_period: %K period
            d_period: %D period
            
        Returns:
            DataFrame with %K and %D values
        """
        if self.has_ta_lib:
            stoch_indicator = ta.momentum.StochasticOscillator(
                high=data['high'], low=data['low'], close=data['close'],
                window=k_period, smooth_window=d_period
            )
            return pd.DataFrame({
                'stoch_k': stoch_indicator.stoch(),
                'stoch_d': stoch_indicator.stoch_signal()
            })
        else:
            # Manual calculation
            lowest_low = data['low'].rolling(window=k_period).min()
            highest_high = data['high'].rolling(window=k_period).max()
            k_percent = 100 * ((data['close'] - lowest_low) / (highest_high - lowest_low))
            d_percent = k_percent.rolling(window=d_period).mean()
            return pd.DataFrame({
                'stoch_k': k_percent,
                'stoch_d': d_percent
            })
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all technical indicators at once
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with all technical indicators
        """
        logger.info("Calculating all technical indicators...")
        
        # Create result dataframe
        result = data.copy()
        
        try:
            # RSI
            result['rsi'] = self.calculate_rsi(data)
            
            # MACD
            macd_data = self.calculate_macd(data)
            result = pd.concat([result, macd_data], axis=1)
            
            # Moving Averages
            ma_data = self.calculate_moving_averages(data)
            result = pd.concat([result, ma_data], axis=1)
            
            # Bollinger Bands
            bb_data = self.calculate_bollinger_bands(data)
            result = pd.concat([result, bb_data], axis=1)
            
            # Stochastic (if OHLC data available)
            if all(col in data.columns for col in ['high', 'low', 'close']):
                stoch_data = self.calculate_stochastic(data)
                result = pd.concat([result, stoch_data], axis=1)
            
            logger.info(f"Successfully calculated indicators for {len(result)} data points")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {str(e)}")
            return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on technical indicators
        
        Args:
            data: DataFrame with technical indicators
            
        Returns:
            DataFrame with trading signals
        """
        signals = pd.DataFrame(index=data.index)
        
        try:
            # RSI signals
            signals['rsi_oversold'] = data['rsi'] < 30
            signals['rsi_overbought'] = data['rsi'] > 70
            
            # MACD signals
            signals['macd_bullish'] = (data['macd'] > data['signal']) & (data['macd'].shift(1) <= data['signal'].shift(1))
            signals['macd_bearish'] = (data['macd'] < data['signal']) & (data['macd'].shift(1) >= data['signal'].shift(1))
            
            # Moving Average signals
            if 'sma_20' in data.columns and 'sma_50' in data.columns:
                signals['ma_golden_cross'] = (data['sma_20'] > data['sma_50']) & (data['sma_20'].shift(1) <= data['sma_50'].shift(1))
                signals['ma_death_cross'] = (data['sma_20'] < data['sma_50']) & (data['sma_20'].shift(1) >= data['sma_50'].shift(1))
            
            # Bollinger Band signals
            if all(col in data.columns for col in ['bb_upper', 'bb_lower']):
                signals['bb_oversold'] = data['close'] < data['bb_lower']
                signals['bb_overbought'] = data['close'] > data['bb_upper']
            
            # Composite signals
            signals['bullish_signals'] = (
                signals.get('rsi_oversold', False) |
                signals.get('macd_bullish', False) |
                signals.get('ma_golden_cross', False) |
                signals.get('bb_oversold', False)
            ).astype(int)
            
            signals['bearish_signals'] = (
                signals.get('rsi_overbought', False) |
                signals.get('macd_bearish', False) |
                signals.get('ma_death_cross', False) |
                signals.get('bb_overbought', False)
            ).astype(int)
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating signals: {str(e)}")
            return pd.DataFrame(index=data.index)

def test_technical_analysis():
    """Test function for technical analysis"""
    print("🧪 Testing Technical Analysis Engine...")
    
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-02-01', freq='D')
    np.random.seed(42)
    
    # Generate realistic stock price data
    returns = np.random.normal(0.001, 0.02, len(dates))
    price = 100
    prices = []
    
    for ret in returns:
        price *= (1 + ret)
        prices.append(price)
    
    sample_data = pd.DataFrame({
        'close': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    # Add open price
    sample_data['open'] = sample_data['close'].shift(1)
    sample_data = sample_data.dropna()
    
    analyzer = TechnicalAnalyzer()
    
    # Test individual indicators
    print("\n📊 Testing individual indicators...")
    rsi = analyzer.calculate_rsi(sample_data)
    print(f"✅ RSI calculated: Latest value = {rsi.iloc[-1]:.2f}")
    
    macd = analyzer.calculate_macd(sample_data)
    print(f"✅ MACD calculated: Latest MACD = {macd['macd'].iloc[-1]:.4f}")
    
    # Test all indicators
    print("\n📈 Testing comprehensive analysis...")
    full_analysis = analyzer.calculate_all_indicators(sample_data)
    print(f"✅ Full analysis: {len(full_analysis.columns)} indicators calculated")
    
    # Test signals
    print("\n🎯 Testing signal generation...")
    signals = analyzer.generate_signals(full_analysis)
    print(f"✅ Signals generated: {signals['bullish_signals'].sum()} bullish, {signals['bearish_signals'].sum()} bearish")

if __name__ == "__main__":
    test_technical_analysis()