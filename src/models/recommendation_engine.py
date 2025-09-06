#!/usr/bin/env python3
"""
Investment Recommendation Engine
Generates buy/sell/hold recommendations based on technical analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    Generates investment recommendations based on technical analysis and market data
    """
    
    def __init__(self, risk_tolerance: str = 'moderate'):
        """
        Initialize recommendation engine
        
        Args:
            risk_tolerance: 'conservative', 'moderate', 'aggressive'
        """
        self.risk_tolerance = risk_tolerance
        self.score_weights = self._get_score_weights()
        logger.info(f"Recommendation Engine initialized (Risk tolerance: {risk_tolerance})")
    
    def _get_score_weights(self) -> Dict[str, float]:
        """
        Get scoring weights based on risk tolerance
        
        Returns:
            Dictionary with indicator weights
        """
        weights = {
            'conservative': {
                'rsi': 0.25,
                'macd': 0.20,
                'moving_averages': 0.30,
                'bollinger_bands': 0.15,
                'volume': 0.10
            },
            'moderate': {
                'rsi': 0.20,
                'macd': 0.25,
                'moving_averages': 0.25,
                'bollinger_bands': 0.20,
                'volume': 0.10
            },
            'aggressive': {
                'rsi': 0.15,
                'macd': 0.30,
                'moving_averages': 0.20,
                'bollinger_bands': 0.25,
                'volume': 0.10
            }
        }
        return weights.get(self.risk_tolerance, weights['moderate'])
    
    def calculate_rsi_score(self, rsi_value: float) -> Tuple[float, str]:
        """
        Calculate RSI-based score
        
        Args:
            rsi_value: Current RSI value
            
        Returns:
            Tuple of (score, reasoning)
        """
        if rsi_value < 30:
            return 0.8, "RSI indicates oversold condition (strong buy signal)"
        elif rsi_value < 40:
            return 0.6, "RSI shows potential buying opportunity"
        elif rsi_value > 70:
            return -0.8, "RSI indicates overbought condition (strong sell signal)"
        elif rsi_value > 60:
            return -0.6, "RSI suggests potential selling opportunity"
        else:
            return 0.0, "RSI in neutral range"
    
    def calculate_macd_score(self, macd_data: pd.Series) -> Tuple[float, str]:
        """
        Calculate MACD-based score
        
        Args:
            macd_data: Series with latest MACD values
            
        Returns:
            Tuple of (score, reasoning)
        """
        if len(macd_data) < 2:
            return 0.0, "Insufficient MACD data"
        
        current_macd = macd_data.iloc[-1]
        current_signal = macd_data.iloc[-1]  # Assuming signal is in same series
        prev_macd = macd_data.iloc[-2]
        
        # Bullish crossover
        if current_macd > 0 and prev_macd <= 0:
            return 0.7, "MACD bullish crossover detected"
        # Bearish crossover
        elif current_macd < 0 and prev_macd >= 0:
            return -0.7, "MACD bearish crossover detected"
        # Above zero line
        elif current_macd > 0:
            return 0.3, "MACD above zero line (bullish momentum)"
        # Below zero line
        elif current_macd < 0:
            return -0.3, "MACD below zero line (bearish momentum)"
        else:
            return 0.0, "MACD neutral"
    
    def calculate_ma_score(self, price: float, ma_data: pd.DataFrame) -> Tuple[float, str]:
        """
        Calculate Moving Average-based score
        
        Args:
            price: Current price
            ma_data: DataFrame with moving averages
            
        Returns:
            Tuple of (score, reasoning)
        """
        scores = []
        reasons = []
        
        # Check short-term MA vs price
        if 'sma_20' in ma_data.columns:
            sma_20 = ma_data['sma_20'].iloc[-1]
            if price > sma_20 * 1.02:  # 2% above
                scores.append(0.5)
                reasons.append("Price well above 20-day SMA")
            elif price > sma_20:
                scores.append(0.3)
                reasons.append("Price above 20-day SMA")
            elif price < sma_20 * 0.98:  # 2% below
                scores.append(-0.5)
                reasons.append("Price well below 20-day SMA")
            else:
                scores.append(-0.3)
                reasons.append("Price below 20-day SMA")
        
        # Check golden/death cross
        if 'sma_20' in ma_data.columns and 'sma_50' in ma_data.columns:
            sma_20_current = ma_data['sma_20'].iloc[-1]
            sma_50_current = ma_data['sma_50'].iloc[-1]
            
            if len(ma_data) > 1:
                sma_20_prev = ma_data['sma_20'].iloc[-2]
                sma_50_prev = ma_data['sma_50'].iloc[-2]
                
                # Golden cross
                if sma_20_current > sma_50_current and sma_20_prev <= sma_50_prev:
                    scores.append(0.8)
                    reasons.append("Golden cross detected (20-day > 50-day MA)")
                # Death cross
                elif sma_20_current < sma_50_current and sma_20_prev >= sma_50_prev:
                    scores.append(-0.8)
                    reasons.append("Death cross detected (20-day < 50-day MA)")
        
        avg_score = np.mean(scores) if scores else 0.0
        combined_reason = "; ".join(reasons) if reasons else "Insufficient MA data"
        
        return avg_score, combined_reason
    
    def calculate_bb_score(self, price: float, bb_data: pd.DataFrame) -> Tuple[float, str]:
        """
        Calculate Bollinger Bands-based score
        
        Args:
            price: Current price
            bb_data: DataFrame with Bollinger Bands
            
        Returns:
            Tuple of (score, reasoning)
        """
        if not all(col in bb_data.columns for col in ['bb_upper', 'bb_lower', 'bb_middle']):
            return 0.0, "Bollinger Bands data not available"
        
        bb_upper = bb_data['bb_upper'].iloc[-1]
        bb_lower = bb_data['bb_lower'].iloc[-1]
        bb_middle = bb_data['bb_middle'].iloc[-1]
        
        # Calculate position within bands
        bb_range = bb_upper - bb_lower
        if bb_range > 0:
            position = (price - bb_lower) / bb_range
            
            if position > 0.8:
                return -0.6, f"Price near upper Bollinger Band ({position:.1%} of range)"
            elif position < 0.2:
                return 0.6, f"Price near lower Bollinger Band ({position:.1%} of range)"
            else:
                return 0.0, f"Price in middle of Bollinger Bands ({position:.1%} of range)"
        else:
            return 0.0, "Bollinger Bands too narrow"
    
    def calculate_volume_score(self, current_volume: float, avg_volume: float) -> Tuple[float, str]:
        """
        Calculate volume-based score
        
        Args:
            current_volume: Current day's volume
            avg_volume: Average volume
            
        Returns:
            Tuple of (score, reasoning)
        """
        if avg_volume == 0:
            return 0.0, "No volume data available"
        
        volume_ratio = current_volume / avg_volume
        
        if volume_ratio > 2.0:
            return 0.4, f"Very high volume ({volume_ratio:.1f}x average) - strong conviction"
        elif volume_ratio > 1.5:
            return 0.2, f"High volume ({volume_ratio:.1f}x average) - good conviction"
        elif volume_ratio < 0.5:
            return -0.2, f"Low volume ({volume_ratio:.1f}x average) - weak conviction"
        else:
            return 0.0, f"Normal volume ({volume_ratio:.1f}x average)"
    
    def generate_recommendation(self, data: pd.DataFrame, stock_info: Dict = None) -> Dict:
        """
        Generate comprehensive recommendation
        
        Args:
            data: DataFrame with price data and technical indicators
            stock_info: Optional stock information
            
        Returns:
            Dictionary with recommendation details
        """
        try:
            logger.info("Generating investment recommendation...")
            
            if data.empty:
                return {'action': 'HOLD', 'confidence': 0, 'reasoning': 'No data available'}
            
            # Get latest values
            latest = data.iloc[-1]
            current_price = latest['close']
            
            # Calculate individual scores
            scores = {}
            reasons = {}
            
            # RSI Score
            if 'rsi' in data.columns:
                rsi_score, rsi_reason = self.calculate_rsi_score(latest['rsi'])
                scores['rsi'] = rsi_score
                reasons['rsi'] = rsi_reason
            
            # MACD Score
            if 'macd' in data.columns:
                macd_score, macd_reason = self.calculate_macd_score(data['macd'].tail(2))
                scores['macd'] = macd_score
                reasons['macd'] = macd_reason
            
            # Moving Average Score
            ma_cols = [col for col in data.columns if 'sma_' in col or 'ema_' in col]
            if ma_cols:
                ma_score, ma_reason = self.calculate_ma_score(current_price, data[ma_cols])
                scores['moving_averages'] = ma_score
                reasons['moving_averages'] = ma_reason
            
            # Bollinger Bands Score
            bb_cols = [col for col in data.columns if 'bb_' in col]
            if bb_cols:
                bb_score, bb_reason = self.calculate_bb_score(current_price, data[bb_cols])
                scores['bollinger_bands'] = bb_score
                reasons['bollinger_bands'] = bb_reason
            
            # Volume Score
            if 'volume' in data.columns and 'volume_ma' in data.columns:
                volume_score, volume_reason = self.calculate_volume_score(
                    latest['volume'], latest.get('volume_ma', latest['volume'])
                )
                scores['volume'] = volume_score
                reasons['volume'] = volume_reason
            
            # Calculate weighted total score
            total_score = 0.0
            total_weight = 0.0
            
            for indicator, score in scores.items():
                weight = self.score_weights.get(indicator, 0.0)
                total_score += score * weight
                total_weight += weight
            
            # Normalize score
            if total_weight > 0:
                final_score = total_score / total_weight
            else:
                final_score = 0.0
            
            # Determine action and confidence with more realistic thresholds
            if final_score > 0.15:
                action = 'BUY'
                confidence = min(95, int(20 + abs(final_score) * 150))
            elif final_score < -0.15:
                action = 'SELL'
                confidence = min(95, int(20 + abs(final_score) * 150))
            else:
                action = 'HOLD'
                confidence = max(50, int(80 - abs(final_score) * 100))
            
            # Calculate position size suggestion
            position_size = self._calculate_position_size(confidence, current_price, stock_info)
            
            # Format detailed reasoning
            detailed_reasoning = []
            for indicator, reason in reasons.items():
                weight = self.score_weights.get(indicator, 0.0)
                detailed_reasoning.append(f"• {indicator.replace('_', ' ').title()} ({weight:.0%}): {reason}")
            
            recommendation = {
                'action': action,
                'confidence': confidence,
                'score': final_score,
                'current_price': current_price,
                'position_size_pct': position_size,
                'reasoning': f"Overall score: {final_score:.2f} → {action} with {confidence}% confidence",
                'detailed_reasoning': detailed_reasoning,
                'individual_scores': scores,
                'risk_tolerance': self.risk_tolerance,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Recommendation generated: {action} ({confidence}% confidence)")
            return recommendation
            
        except Exception as e:
            logger.error(f"Error generating recommendation: {str(e)}")
            return {
                'action': 'HOLD',
                'confidence': 0,
                'reasoning': f'Error in analysis: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_position_size(self, confidence: int, price: float, stock_info: Dict = None) -> float:
        """
        Calculate suggested position size based on confidence and risk tolerance
        
        Args:
            confidence: Confidence level (0-100)
            price: Current stock price
            stock_info: Optional stock information
            
        Returns:
            Suggested position size as percentage of portfolio
        """
        base_sizes = {
            'conservative': 5.0,
            'moderate': 10.0,
            'aggressive': 15.0
        }
        
        base_size = base_sizes.get(self.risk_tolerance, 10.0)
        
        # Adjust based on confidence
        confidence_multiplier = confidence / 100.0
        
        # Adjust based on volatility if available
        volatility_adjustment = 1.0
        if stock_info and 'beta' in stock_info:
            beta = stock_info.get('beta', 1.0)
            if beta > 1.5:  # High volatility
                volatility_adjustment = 0.7
            elif beta < 0.7:  # Low volatility
                volatility_adjustment = 1.2
        
        position_size = base_size * confidence_multiplier * volatility_adjustment
        
        # Cap position size
        max_size = {'conservative': 10, 'moderate': 20, 'aggressive': 25}
        return min(position_size, max_size.get(self.risk_tolerance, 20))

def test_recommendation_engine():
    """Test function for recommendation engine"""
    print("🧪 Testing Recommendation Engine...")
    
    # Create sample data with indicators
    dates = pd.date_range(start='2024-01-01', end='2024-02-01', freq='D')
    np.random.seed(42)
    
    sample_data = pd.DataFrame({
        'close': np.random.normal(100, 10, len(dates)),
        'volume': np.random.randint(1000000, 10000000, len(dates)),
        'rsi': np.random.normal(50, 15, len(dates)),
        'macd': np.random.normal(0, 0.5, len(dates)),
        'sma_20': np.random.normal(100, 8, len(dates)),
        'sma_50': np.random.normal(100, 6, len(dates)),
        'bb_upper': np.random.normal(110, 5, len(dates)),
        'bb_lower': np.random.normal(90, 5, len(dates)),
        'bb_middle': np.random.normal(100, 3, len(dates)),
        'volume_ma': np.random.randint(2000000, 8000000, len(dates))
    }, index=dates)
    
    # Test different risk tolerances
    for risk_tolerance in ['conservative', 'moderate', 'aggressive']:
        print(f"\n📊 Testing {risk_tolerance} risk tolerance...")
        
        engine = RecommendationEngine(risk_tolerance=risk_tolerance)
        recommendation = engine.generate_recommendation(sample_data)
        
        print(f"   Action: {recommendation['action']}")
        print(f"   Confidence: {recommendation['confidence']}%")
        print(f"   Position Size: {recommendation.get('position_size_pct', 0):.1f}%")
        print(f"   Score: {recommendation['score']:.3f}")

if __name__ == "__main__":
    test_recommendation_engine()