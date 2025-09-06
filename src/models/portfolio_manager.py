#!/usr/bin/env python3
"""
Portfolio Manager
Manual portfolio management - user inputs real positions, system provides TA analysis for holdings
"""

from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import logging

from .portfolio_tracker import PortfolioTracker, Position, Transaction
from ..data.market_data import MarketDataFetcher
from ..analyzers.technical_analysis import TechnicalAnalyzer
from .recommendation_engine import RecommendationEngine

class PortfolioManager:
    """
    High-level portfolio management interface
    Combines portfolio tracking with market data and analysis
    """
    
    def __init__(self, initial_cash: float = 50000):
        """
        Initialize manual portfolio manager
        
        Args:
            initial_cash: User's actual cash balance (manually entered)
        """
        self.tracker = PortfolioTracker()
        self.market_data = MarketDataFetcher()
        self.technical_analyzer = TechnicalAnalyzer()
        
        self.cash_balance = initial_cash  # User manually updates this
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Manual portfolio manager initialized - user controls all entries")
        
    def update_cash_balance(self, new_balance: float, notes: str = None):
        """Update cash balance manually (user enters actual balance)"""
        old_balance = self.cash_balance
        self.cash_balance = new_balance
        self.logger.info(f"Cash balance updated manually: ${old_balance:,.2f} → ${new_balance:,.2f}")
        if notes:
            self.logger.info(f"Notes: {notes}")
    
    def get_current_prices(self, symbols: List[str] = None) -> Dict[str, float]:
        """Get current prices for portfolio positions or specified symbols"""
        if not symbols:
            # Get symbols from current positions
            positions = self.tracker.get_positions({})  # Empty dict for cached symbols
            symbols = [pos.symbol for pos in positions]
        
        if not symbols:
            return {}
        
        current_prices = {}
        for symbol in symbols:
            try:
                data = self.market_data.get_stock_data(symbol, period='1d')
                if not data.empty:
                    current_prices[symbol] = float(data['close'].iloc[-1])
                else:
                    self.logger.warning(f"No current price data for {symbol}")
            except Exception as e:
                self.logger.error(f"Error fetching price for {symbol}: {e}")
        
        return current_prices
    
    def get_portfolio_status(self) -> Dict[str, Any]:
        """Get comprehensive portfolio status"""
        # Get current prices for all positions
        current_prices = self.get_current_prices()
        
        # Get portfolio summary
        summary = self.tracker.get_portfolio_summary(current_prices, self.cash_balance)
        
        # Add additional analysis
        positions = self.tracker.get_positions(current_prices)
        
        # Calculate portfolio allocation
        total_value = summary['total_portfolio_value']
        allocations = {}
        if positions and total_value > 0:
            for pos in positions:
                allocations[pos.symbol] = (pos.market_value / total_value) * 100
        
        # Add risk metrics
        risk_metrics = self._calculate_portfolio_risk(positions, current_prices)
        
        return {
            **summary,
            'cash_percentage': (self.cash_balance / total_value * 100) if total_value > 0 else 100,
            'position_allocations': allocations,
            'risk_metrics': risk_metrics,
            'testing_mode': self.testing_mode,
            'testing_duration_days': (datetime.now() - self.testing_start_date).days if self.testing_mode else None
        }
    
    def analyze_and_recommend(self, symbol: str, risk_tolerance: str = 'moderate') -> Dict[str, Any]:
        """
        Analyze a stock and generate recommendation
        Uses existing TA analyzer for consistency with main analysis feature
        """
        try:
            # Fetch market data
            data = self.market_data.get_stock_data(symbol, period='3mo')
            stock_info = self.market_data.get_stock_info(symbol)
            
            if data.empty:
                return {
                    'success': False,
                    'error': f'No market data available for {symbol}',
                    'symbol': symbol
                }
            
            # Perform technical analysis using existing TA analyzer
            analysis = self.technical_analyzer.calculate_all_indicators(data)
            
            # Generate recommendation using existing recommendation engine
            engine = RecommendationEngine(risk_tolerance=risk_tolerance)
            recommendation = engine.generate_recommendation(analysis, stock_info)
            
            # Store recommendation for tracking
            recommendation_id = self.tracker.add_recommendation(
                symbol=symbol,
                action=recommendation['action'],
                confidence=recommendation['confidence'],
                reasoning=recommendation['reasoning'],
                target_price=recommendation.get('target_price'),
                stop_loss=recommendation.get('stop_loss')
            )
            
            # Calculate position sizing if it's a BUY recommendation
            position_size = None
            if recommendation['action'] == 'BUY':
                position_size = self._calculate_position_size(
                    symbol, 
                    float(analysis['close'].iloc[-1]), 
                    recommendation['confidence'],
                    risk_tolerance
                )
            
            return {
                'success': True,
                'symbol': symbol,
                'recommendation_id': recommendation_id,
                'action': recommendation['action'],
                'confidence': recommendation['confidence'],
                'reasoning': recommendation['reasoning'],
                'current_price': float(analysis['close'].iloc[-1]),
                'target_price': recommendation.get('target_price'),
                'stop_loss': recommendation.get('stop_loss'),
                'position_size': position_size,
                'technical_data': {
                    'rsi': float(analysis['rsi'].iloc[-1]),
                    'sma_20': float(analysis['sma_20'].iloc[-1]),
                    'sma_50': float(analysis['sma_50'].iloc[-1]),
                    'macd': float(analysis['macd'].iloc[-1]),
                    'bb_position': 'upper' if analysis['close'].iloc[-1] > analysis['bb_upper'].iloc[-1] else 
                                  'lower' if analysis['close'].iloc[-1] < analysis['bb_lower'].iloc[-1] else 'middle'
                },
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing {symbol}: {e}")
            return {
                'success': False,
                'error': str(e),
                'symbol': symbol
            }
    
    def execute_recommendation(self, recommendation_id: str, quantity: float = None, 
                             notes: str = None) -> Dict[str, Any]:
        """
        Execute a recommendation (for testing or real trading)
        """
        try:
            # Get recommendation details from database
            with sqlite3.connect(self.tracker.db_path) as conn:
                cursor = conn.execute(
                    "SELECT * FROM recommendations WHERE recommendation_id = ?", 
                    (recommendation_id,)
                )
                rec_data = cursor.fetchone()
            
            if not rec_data:
                return {
                    'success': False,
                    'error': f'Recommendation {recommendation_id} not found'
                }
            
            symbol = rec_data[1]
            action = rec_data[2]
            confidence = rec_data[3]
            
            # Get current price
            current_prices = self.get_current_prices([symbol])
            if symbol not in current_prices:
                return {
                    'success': False,
                    'error': f'Unable to get current price for {symbol}'
                }
            
            current_price = current_prices[symbol]
            
            # Calculate quantity if not provided
            if quantity is None:
                if action == 'BUY':
                    position_size = self._calculate_position_size(symbol, current_price, confidence)
                    quantity = position_size['shares']
                else:  # SELL
                    # Sell current position
                    positions = self.tracker.get_positions(current_prices)
                    current_position = next((p for p in positions if p.symbol == symbol), None)
                    if not current_position:
                        return {
                            'success': False,
                            'error': f'No position in {symbol} to sell'
                        }
                    quantity = current_position.quantity
            
            # Calculate commission
            commission = abs(quantity * current_price * self.commission_rate)
            
            # Check if we have enough cash for BUY orders
            if action == 'BUY':
                total_cost = (quantity * current_price) + commission
                if total_cost > self.cash_balance:
                    return {
                        'success': False,
                        'error': f'Insufficient cash. Need ${total_cost:,.2f}, have ${self.cash_balance:,.2f}'
                    }
            
            # Execute transaction
            transaction_id = self.tracker.execute_transaction(
                symbol=symbol,
                action=action,
                quantity=quantity,
                price=current_price,
                commission=commission,
                recommendation_id=recommendation_id,
                notes=notes or f"{'Test' if self.testing_mode else 'Live'} execution of recommendation"
            )
            
            # Update cash balance
            if action == 'BUY':
                self.cash_balance -= (quantity * current_price) + commission
            else:  # SELL
                self.cash_balance += (quantity * current_price) - commission
            
            return {
                'success': True,
                'transaction_id': transaction_id,
                'symbol': symbol,
                'action': action,
                'quantity': quantity,
                'price': current_price,
                'commission': commission,
                'new_cash_balance': self.cash_balance,
                'testing_mode': self.testing_mode
            }
            
        except Exception as e:
            self.logger.error(f"Error executing recommendation {recommendation_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_position_size(self, symbol: str, price: float, confidence: float, 
                               risk_tolerance: str = 'moderate') -> Dict[str, Any]:
        """Calculate appropriate position size based on risk and confidence"""
        
        # Base allocation percentages by risk tolerance
        base_allocations = {
            'conservative': 0.05,  # 5% max per position
            'moderate': 0.10,      # 10% max per position
            'aggressive': 0.15     # 15% max per position
        }
        
        base_allocation = base_allocations.get(risk_tolerance, 0.10)
        
        # Adjust by confidence (scale from 0.5x to 1.5x based on confidence)
        confidence_multiplier = 0.5 + (confidence / 100)  # 50-100% confidence -> 1.0-1.5x
        
        # Calculate position size
        portfolio_value = self.cash_balance + sum(
            pos.market_value for pos in self.tracker.get_positions(self.get_current_prices())
        )
        
        target_allocation = base_allocation * confidence_multiplier
        target_value = portfolio_value * target_allocation
        
        # Ensure we don't exceed cash balance
        max_value = min(target_value, self.cash_balance * 0.95)  # Leave 5% cash buffer
        
        shares = int(max_value / price)
        actual_cost = shares * price
        actual_allocation = (actual_cost / portfolio_value) * 100 if portfolio_value > 0 else 0
        
        return {
            'shares': shares,
            'cost': actual_cost,
            'target_allocation_pct': target_allocation * 100,
            'actual_allocation_pct': actual_allocation,
            'confidence_multiplier': confidence_multiplier,
            'price_per_share': price
        }
    
    def _calculate_portfolio_risk(self, positions: List[Position], current_prices: Dict[str, float]) -> Dict[str, float]:
        """Calculate portfolio risk metrics"""
        if not positions:
            return {'concentration_risk': 0, 'largest_position_pct': 0, 'position_count': 0}
        
        total_value = sum(pos.market_value for pos in positions)
        
        # Concentration risk (largest position percentage)
        largest_position_pct = max(pos.market_value / total_value * 100 for pos in positions) if total_value > 0 else 0
        
        # Simple concentration risk score
        concentration_risk = largest_position_pct / 20  # Normalized to 20% as "normal" max
        
        return {
            'concentration_risk': min(concentration_risk, 5.0),  # Cap at 5.0 (very high risk)
            'largest_position_pct': largest_position_pct,
            'position_count': len(positions)
        }
    
    def get_testing_report(self) -> Dict[str, Any]:
        """Generate comprehensive testing report for accuracy assessment"""
        if not self.testing_mode:
            return {'error': 'Not in testing mode'}
        
        # Get all recommendations since testing started
        with sqlite3.connect(self.tracker.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM recommendations 
                WHERE timestamp >= ? 
                ORDER BY timestamp DESC
            """, (self.testing_start_date.isoformat(),))
            
            recommendations = cursor.fetchall()
        
        # Get performance metrics
        performance = self.tracker.get_performance_metrics(
            days=(datetime.now() - self.testing_start_date).days + 1
        )
        
        # Calculate recommendation accuracy (placeholder - would need price tracking)
        total_recs = len(recommendations)
        executed_recs = sum(1 for rec in recommendations if rec[8])  # executed column
        
        # Get current portfolio status
        portfolio_status = self.get_portfolio_status()
        
        # Calculate total return
        initial_value = 100000  # This should be tracked from start
        current_value = portfolio_status['total_portfolio_value']
        total_return = ((current_value - initial_value) / initial_value) * 100
        
        return {
            'testing_duration_days': (datetime.now() - self.testing_start_date).days,
            'total_recommendations': total_recs,
            'executed_recommendations': executed_recs,
            'execution_rate_pct': (executed_recs / total_recs * 100) if total_recs > 0 else 0,
            'initial_balance': initial_value,
            'current_value': current_value,
            'total_return_pct': total_return,
            'performance_metrics': performance,
            'portfolio_status': portfolio_status,
            'recommendations_by_action': {
                'BUY': sum(1 for rec in recommendations if rec[2] == 'BUY'),
                'SELL': sum(1 for rec in recommendations if rec[2] == 'SELL'),
                'HOLD': sum(1 for rec in recommendations if rec[2] == 'HOLD')
            },
            'avg_confidence': np.mean([rec[3] for rec in recommendations]) if recommendations else 0,
            'testing_start_date': self.testing_start_date,
            'report_generated': datetime.now()
        }
    
    def save_daily_snapshot(self):
        """Save daily portfolio snapshot for tracking"""
        current_prices = self.get_current_prices()
        self.tracker.save_portfolio_snapshot(current_prices, self.cash_balance)
        self.logger.info("Daily portfolio snapshot saved")

# Test function
if __name__ == "__main__":
    # Example usage
    manager = PortfolioManager(initial_cash=50000)
    manager.set_testing_mode(True)
    
    # Analyze a stock
    result = manager.analyze_and_recommend("AAPL", "moderate")
    print("Analysis Result:", result)
    
    # Get portfolio status
    status = manager.get_portfolio_status()
    print("\nPortfolio Status:")
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    # Generate testing report
    report = manager.get_testing_report()
    print("\nTesting Report:")
    for key, value in report.items():
        if not isinstance(value, dict):
            print(f"  {key}: {value}")
