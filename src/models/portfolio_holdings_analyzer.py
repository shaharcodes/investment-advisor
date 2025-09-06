#!/usr/bin/env python3
"""
Portfolio Holdings Analyzer
Analyzes user's actual portfolio holdings using existing TA analyzer
"""

from typing import Dict, List, Any
import pandas as pd
from datetime import datetime
import logging

from .portfolio_tracker import PortfolioTracker
from ..data.market_data import MarketDataFetcher
from ..analyzers.technical_analysis import TechnicalAnalyzer
from .recommendation_engine import RecommendationEngine

class PortfolioHoldingsAnalyzer:
    """
    Analyzes actual portfolio holdings using existing TA analyzer
    Provides recommendations for currently owned stocks only
    """
    
    def __init__(self, portfolio_tracker: PortfolioTracker):
        """Initialize with portfolio tracker and existing analyzers"""
        self.tracker = portfolio_tracker
        self.market_data = MarketDataFetcher()
        self.technical_analyzer = TechnicalAnalyzer()  # Use existing TA analyzer
        self.logger = logging.getLogger(__name__)
    
    def analyze_all_holdings(self, current_prices: Dict[str, float], risk_tolerance: str = 'moderate') -> Dict[str, Any]:
        """
        Analyze ALL current portfolio holdings using existing TA analyzer
        
        Args:
            current_prices: Current market prices for portfolio positions
            risk_tolerance: Risk profile for recommendations
            
        Returns:
            Dict with TA analysis and recommendations for each holding
        """
        # Get current positions from tracker
        positions = self.tracker.get_positions(current_prices)
        
        if not positions:
            return {
                'holdings_analysis': {},
                'summary': {
                    'total_holdings': 0,
                    'message': 'No positions to analyze'
                }
            }
        
        holdings_analysis = {}
        
        for position in positions:
            symbol = position.symbol
            
            try:
                # Analyze this holding using existing TA analyzer
                analysis = self.analyze_single_holding(
                    symbol=symbol,
                    position=position,
                    risk_tolerance=risk_tolerance
                )
                
                holdings_analysis[symbol] = analysis
                
            except Exception as e:
                self.logger.error(f"Error analyzing holding {symbol}: {e}")
                holdings_analysis[symbol] = {
                    'success': False,
                    'error': str(e),
                    'symbol': symbol
                }
        
        # Generate summary
        summary = self._generate_holdings_summary(holdings_analysis)
        
        return {
            'holdings_analysis': holdings_analysis,
            'summary': summary,
            'analysis_timestamp': datetime.now()
        }
    
    def analyze_single_holding(self, symbol: str, position, risk_tolerance: str = 'moderate') -> Dict[str, Any]:
        """
        Analyze a single holding using existing TA analyzer
        Uses same technical analysis as main TA feature
        """
        try:
            # Fetch market data (same period as main TA feature)
            data = self.market_data.get_stock_data(symbol, period='3mo')
            stock_info = self.market_data.get_stock_info(symbol)
            
            if data.empty:
                return {
                    'success': False,
                    'error': f'No market data available for {symbol}',
                    'symbol': symbol
                }
            
            # Use existing TechnicalAnalyzer (same logic as main TA feature)
            analysis = self.technical_analyzer.calculate_all_indicators(data)
            
            # Generate recommendation using existing engine
            engine = RecommendationEngine(risk_tolerance=risk_tolerance)
            recommendation = engine.generate_recommendation(analysis, stock_info)
            
            # Add portfolio-specific context
            holding_analysis = {
                **recommendation,  # Include all standard TA recommendation fields
                'success': True,
                'symbol': symbol,
                'current_price': position.current_price,
                'holding_details': {
                    'quantity': position.quantity,
                    'avg_cost': position.avg_cost,
                    'market_value': position.market_value,
                    'unrealized_pnl': position.unrealized_pnl,
                    'unrealized_pnl_pct': position.unrealized_pnl_pct,
                    'entry_date': position.entry_date.strftime('%Y-%m-%d')
                },
                'position_advice': self._generate_position_advice(
                    recommendation['action'],
                    recommendation['confidence'],
                    position.unrealized_pnl_pct,
                    position.quantity
                ),
                'technical_summary': {
                    'rsi': float(analysis['rsi'].iloc[-1]),
                    'sma_20': float(analysis['sma_20'].iloc[-1]),
                    'sma_50': float(analysis['sma_50'].iloc[-1]),
                    'macd': float(analysis['macd'].iloc[-1]),
                    'bb_position': self._get_bollinger_position(analysis),
                    'trend': 'bullish' if analysis['close'].iloc[-1] > analysis['sma_20'].iloc[-1] else 'bearish'
                },
                'analysis_timestamp': datetime.now()
            }
            
            return holding_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing holding {symbol}: {e}")
            return {
                'success': False,
                'error': str(e),
                'symbol': symbol
            }
    
    def _generate_position_advice(self, action: str, confidence: float, 
                                current_pnl_pct: float, current_quantity: float) -> str:
        """Generate position-specific advice for owned stocks"""
        
        if action == 'BUY':
            if confidence > 75:
                add_qty = max(int(current_quantity * 0.25), 10)
                return f"Strong BUY signal - consider adding ~{add_qty} shares to position"
            elif confidence > 60:
                add_qty = max(int(current_quantity * 0.15), 5)
                return f"Moderate BUY signal - consider adding ~{add_qty} shares"
            else:
                return "Weak BUY signal - hold current position, monitor for stronger signals"
        
        elif action == 'SELL':
            if confidence > 75:
                if current_pnl_pct > 10:
                    return "Strong SELL signal - consider taking profits, reduce position by 50-75%"
                else:
                    return "Strong SELL signal - consider reducing position to limit losses"
            elif confidence > 60:
                reduce_qty = max(int(current_quantity * 0.3), 10)
                return f"Moderate SELL signal - consider reducing by ~{reduce_qty} shares"
            else:
                return "Weak SELL signal - monitor closely, consider partial profit-taking if profitable"
        
        else:  # HOLD
            if current_pnl_pct > 20:
                return "HOLD - strong position, consider taking some profits at these levels"
            elif current_pnl_pct < -15:
                return "HOLD - position underwater, monitor for recovery or consider stop-loss"
            else:
                return "HOLD - maintain current position, await clearer signals"
    
    def _get_bollinger_position(self, analysis: pd.DataFrame) -> str:
        """Determine price position relative to Bollinger Bands"""
        latest = analysis.iloc[-1]
        price = latest['close']
        bb_upper = latest['bb_upper']
        bb_lower = latest['bb_lower']
        
        if price > bb_upper:
            return 'overbought'
        elif price < bb_lower:
            return 'oversold'
        else:
            return 'normal'
    
    def _generate_holdings_summary(self, holdings_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of recommendations across all holdings"""
        
        buy_signals = []
        sell_signals = []
        hold_signals = []
        errors = []
        total_confidence = 0
        successful_analyses = 0
        
        for symbol, analysis in holdings_analysis.items():
            if analysis.get('success'):
                successful_analyses += 1
                action = analysis['action']
                confidence = analysis['confidence']
                total_confidence += confidence
                
                signal_info = {
                    'symbol': symbol,
                    'confidence': confidence,
                    'pnl_pct': analysis['holding_details']['unrealized_pnl_pct']
                }
                
                if action == 'BUY':
                    buy_signals.append(signal_info)
                elif action == 'SELL':
                    sell_signals.append(signal_info)
                else:
                    hold_signals.append(signal_info)
            else:
                errors.append({
                    'symbol': symbol,
                    'error': analysis.get('error', 'Unknown error')
                })
        
        avg_confidence = total_confidence / successful_analyses if successful_analyses > 0 else 0
        
        # Find strongest signals
        strongest_buy = max(buy_signals, key=lambda x: x['confidence']) if buy_signals else None
        strongest_sell = max(sell_signals, key=lambda x: x['confidence']) if sell_signals else None
        
        return {
            'total_holdings': len(holdings_analysis),
            'successful_analyses': successful_analyses,
            'buy_signals': len(buy_signals),
            'sell_signals': len(sell_signals),
            'hold_signals': len(hold_signals),
            'errors': len(errors),
            'avg_confidence': avg_confidence,
            'strongest_buy': strongest_buy,
            'strongest_sell': strongest_sell,
            'error_details': errors
        }

# Test function  
if __name__ == "__main__":
    # Example usage for testing
    from .portfolio_tracker import PortfolioTracker
    
    # Create tracker and analyzer
    tracker = PortfolioTracker("test_portfolio.db")
    analyzer = PortfolioHoldingsAnalyzer(tracker)
    
    # Test with sample current prices
    current_prices = {
        'AAPL': 165.50,
        'MSFT': 275.30
    }
    
    try:
        results = analyzer.analyze_all_holdings(current_prices, 'moderate')
        
        print("Portfolio Holdings Analysis:")
        print(f"Total Holdings: {results['summary']['total_holdings']}")
        print(f"BUY signals: {results['summary']['buy_signals']}")
        print(f"SELL signals: {results['summary']['sell_signals']}")
        print(f"HOLD signals: {results['summary']['hold_signals']}")
        print(f"Average confidence: {results['summary']['avg_confidence']:.1f}%")
        
        for symbol, analysis in results['holdings_analysis'].items():
            if analysis.get('success'):
                print(f"\n{symbol}: {analysis['action']} ({analysis['confidence']}%)")
                print(f"  P&L: {analysis['holding_details']['unrealized_pnl_pct']:.1f}%")
                print(f"  Advice: {analysis['position_advice']}")
            else:
                print(f"\n{symbol}: Analysis failed - {analysis.get('error')}")
                
    except Exception as e:
        print(f"Test failed: {e}")
