#!/usr/bin/env python3
"""
Portfolio Analyzer
Integrates existing TA analyzer with portfolio holdings for recommendations
"""

from typing import Dict, List, Any
import pandas as pd
from datetime import datetime
import logging

from ..data.market_data import MarketDataFetcher
from ..analyzers.technical_analysis import TechnicalAnalyzer
from .recommendation_engine import RecommendationEngine

class PortfolioAnalyzer:
    """
    Analyzes portfolio holdings using existing TA analyzer
    Generates recommendations for currently owned stocks
    """
    
    def __init__(self):
        """Initialize with existing analyzers"""
        self.market_data = MarketDataFetcher()
        self.technical_analyzer = TechnicalAnalyzer()
        self.logger = logging.getLogger(__name__)
    
    def analyze_holdings(self, holdings: List[Dict[str, Any]], risk_tolerance: str = 'moderate') -> Dict[str, Any]:
        """
        Analyze all portfolio holdings using existing TA analyzer
        
        Args:
            holdings: List of portfolio positions [{symbol, quantity, avg_cost, ...}]
            risk_tolerance: Risk profile for recommendations
            
        Returns:
            Dict with analysis results for each holding
        """
        results = {}
        
        for holding in holdings:
            symbol = holding['symbol']
            
            try:
                # Use existing TA analyzer for this holding
                analysis_result = self.analyze_single_holding(
                    symbol=symbol,
                    quantity=holding['quantity'],
                    avg_cost=holding['avg_cost'],
                    risk_tolerance=risk_tolerance
                )
                
                results[symbol] = analysis_result
                
            except Exception as e:
                self.logger.error(f"Error analyzing {symbol}: {e}")
                results[symbol] = {
                    'success': False,
                    'error': str(e),
                    'symbol': symbol
                }
        
        return results
    
    def analyze_single_holding(self, symbol: str, quantity: float, avg_cost: float, 
                              risk_tolerance: str = 'moderate') -> Dict[str, Any]:
        """
        Analyze a single holding using existing TA analyzer
        Same logic as main TA feature but focused on owned stocks
        """
        try:
            # Fetch market data (same as main TA feature)
            data = self.market_data.get_stock_data(symbol, period='3mo')
            stock_info = self.market_data.get_stock_info(symbol)
            
            if data.empty:
                return {
                    'success': False,
                    'error': f'No market data available for {symbol}',
                    'symbol': symbol
                }
            
            # Use existing technical analyzer (exact same implementation)
            analysis = self.technical_analyzer.calculate_all_indicators(data)
            
            # Generate recommendation using existing engine
            engine = RecommendationEngine(risk_tolerance=risk_tolerance)
            recommendation = engine.generate_recommendation(analysis, stock_info)
            
            # Calculate holding-specific metrics
            current_price = float(analysis['close'].iloc[-1])
            market_value = quantity * current_price
            cost_basis = quantity * avg_cost
            unrealized_pnl = market_value - cost_basis
            unrealized_pnl_pct = (unrealized_pnl / cost_basis) * 100 if cost_basis > 0 else 0
            
            # Add position context to recommendation
            recommendation_with_context = {
                **recommendation,
                'success': True,
                'symbol': symbol,
                'current_price': current_price,
                'holding_info': {
                    'quantity': quantity,
                    'avg_cost': avg_cost,
                    'market_value': market_value,
                    'cost_basis': cost_basis,
                    'unrealized_pnl': unrealized_pnl,
                    'unrealized_pnl_pct': unrealized_pnl_pct
                },
                'position_suggestion': self._generate_position_suggestion(
                    recommendation['action'], 
                    recommendation['confidence'],
                    unrealized_pnl_pct,
                    quantity
                ),
                'technical_data': {
                    'rsi': float(analysis['rsi'].iloc[-1]),
                    'sma_20': float(analysis['sma_20'].iloc[-1]),
                    'sma_50': float(analysis['sma_50'].iloc[-1]),
                    'macd': float(analysis['macd'].iloc[-1]),
                    'bb_position': self._get_bollinger_position(analysis)
                },
                'timestamp': datetime.now()
            }
            
            return recommendation_with_context
            
        except Exception as e:
            self.logger.error(f"Error analyzing holding {symbol}: {e}")
            return {
                'success': False,
                'error': str(e),
                'symbol': symbol
            }
    
    def _generate_position_suggestion(self, action: str, confidence: float, 
                                    current_pnl_pct: float, current_quantity: float) -> str:
        """Generate position-specific suggestions for owned stocks"""
        
        if action == 'BUY':
            if confidence > 75:
                return f"Strong BUY signal - consider adding 25-50% to position ({int(current_quantity * 0.25)}-{int(current_quantity * 0.5)} shares)"
            elif confidence > 60:
                return f"Moderate BUY signal - consider adding 10-25% to position ({int(current_quantity * 0.1)}-{int(current_quantity * 0.25)} shares)"
            else:
                return "Weak BUY signal - hold current position, consider small addition if conviction is high"
        
        elif action == 'SELL':
            if confidence > 75:
                return "Strong SELL signal - consider reducing position by 50-75% or exiting completely"
            elif confidence > 60:
                return "Moderate SELL signal - consider reducing position by 25-50%"
            else:
                return "Weak SELL signal - consider taking partial profits if position is profitable"
        
        else:  # HOLD
            if current_pnl_pct > 20:
                return "HOLD - position is profitable, consider taking partial profits if needed"
            elif current_pnl_pct < -10:
                return "HOLD - position is down, monitor for improvement or consider stop-loss"
            else:
                return "HOLD - maintain current position size"
    
    def _get_bollinger_position(self, analysis: pd.DataFrame) -> str:
        """Determine price position relative to Bollinger Bands"""
        latest = analysis.iloc[-1]
        price = latest['close']
        bb_upper = latest['bb_upper']
        bb_lower = latest['bb_lower']
        
        if price > bb_upper:
            return 'above_upper'
        elif price < bb_lower:
            return 'below_lower'
        else:
            return 'between_bands'
    
    def get_portfolio_recommendation_summary(self, holdings_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary of recommendations across all holdings
        """
        buy_signals = []
        sell_signals = []
        hold_signals = []
        total_positions = 0
        avg_confidence = 0
        
        for symbol, analysis in holdings_analysis.items():
            if analysis.get('success'):
                total_positions += 1
                action = analysis['action']
                confidence = analysis['confidence']
                
                avg_confidence += confidence
                
                if action == 'BUY':
                    buy_signals.append({'symbol': symbol, 'confidence': confidence})
                elif action == 'SELL':
                    sell_signals.append({'symbol': symbol, 'confidence': confidence})
                else:
                    hold_signals.append({'symbol': symbol, 'confidence': confidence})
        
        avg_confidence = avg_confidence / total_positions if total_positions > 0 else 0
        
        return {
            'total_positions_analyzed': total_positions,
            'buy_signals': len(buy_signals),
            'sell_signals': len(sell_signals),
            'hold_signals': len(hold_signals),
            'avg_confidence': avg_confidence,
            'strongest_buy': max(buy_signals, key=lambda x: x['confidence']) if buy_signals else None,
            'strongest_sell': max(sell_signals, key=lambda x: x['confidence']) if sell_signals else None,
            'analysis_timestamp': datetime.now()
        }

# Test function
if __name__ == "__main__":
    # Example usage
    analyzer = PortfolioAnalyzer()
    
    # Test with sample holdings
    sample_holdings = [
        {'symbol': 'AAPL', 'quantity': 100, 'avg_cost': 150.0},
        {'symbol': 'MSFT', 'quantity': 50, 'avg_cost': 280.0}
    ]
    
    try:
        results = analyzer.analyze_holdings(sample_holdings, 'moderate')
        
        print("Portfolio Analysis Results:")
        for symbol, analysis in results.items():
            if analysis.get('success'):
                print(f"\n{symbol}:")
                print(f"  Action: {analysis['action']} ({analysis['confidence']}%)")
                print(f"  Current P&L: {analysis['holding_info']['unrealized_pnl_pct']:.1f}%")
                print(f"  Suggestion: {analysis['position_suggestion']}")
            else:
                print(f"\n{symbol}: Analysis failed - {analysis.get('error', 'Unknown error')}")
        
        # Summary
        summary = analyzer.get_portfolio_recommendation_summary(results)
        print(f"\nPortfolio Summary:")
        print(f"  BUY signals: {summary['buy_signals']}")
        print(f"  SELL signals: {summary['sell_signals']}")
        print(f"  HOLD signals: {summary['hold_signals']}")
        print(f"  Average confidence: {summary['avg_confidence']:.1f}%")
        
    except Exception as e:
        print(f"Test failed: {e}")
