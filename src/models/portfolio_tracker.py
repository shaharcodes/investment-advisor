#!/usr/bin/env python3
"""
Portfolio Tracker  
Manual portfolio tracking system - user enters positions from real brokerage accounts
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Position:
    """Represents a portfolio position"""
    symbol: str
    quantity: float
    avg_cost: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    entry_date: datetime
    last_updated: datetime

@dataclass
class Transaction:
    """Represents a transaction (buy/sell)"""
    transaction_id: str
    symbol: str
    action: str  # 'BUY', 'SELL'
    quantity: float
    price: float
    total_cost: float
    commission: float
    timestamp: datetime
    recommendation_id: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class Recommendation:
    """Represents an AI recommendation and its outcome"""
    recommendation_id: str
    symbol: str
    action: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float
    reasoning: str
    target_price: Optional[float]
    stop_loss: Optional[float]
    timestamp: datetime
    executed: bool = False
    execution_price: Optional[float] = None
    execution_date: Optional[datetime] = None
    outcome_score: Optional[float] = None  # For learning

class PortfolioTracker:
    """
    Comprehensive portfolio tracking system
    Handles positions, transactions, performance metrics, and recommendation tracking
    """
    
    def __init__(self, db_path: str = "data/portfolio.db"):
        """Initialize portfolio tracker with database"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self._init_database()
        
        # Cache for performance
        self._positions_cache: Dict[str, Position] = {}
        self._cache_expiry = datetime.now()
        
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            # Positions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS positions (
                    symbol TEXT PRIMARY KEY,
                    quantity REAL NOT NULL,
                    avg_cost REAL NOT NULL,
                    entry_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL
                )
            """)
            
            # Transactions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    symbol TEXT NOT NULL,
                    action TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    price REAL NOT NULL,
                    total_cost REAL NOT NULL,
                    commission REAL DEFAULT 0,
                    timestamp TEXT NOT NULL,
                    recommendation_id TEXT,
                    notes TEXT
                )
            """)
            
            # Recommendations table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recommendations (
                    recommendation_id TEXT PRIMARY KEY,
                    symbol TEXT NOT NULL,
                    action TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    reasoning TEXT,
                    target_price REAL,
                    stop_loss REAL,
                    timestamp TEXT NOT NULL,
                    executed INTEGER DEFAULT 0,
                    execution_price REAL,
                    execution_date TEXT,
                    outcome_score REAL
                )
            """)
            
            # Portfolio snapshots for performance tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    total_value REAL NOT NULL,
                    cash_balance REAL NOT NULL,
                    positions_value REAL NOT NULL,
                    total_pnl REAL NOT NULL,
                    daily_return REAL,
                    positions_json TEXT NOT NULL
                )
            """)
            
            conn.commit()
    
    def add_recommendation(self, symbol: str, action: str, confidence: float, 
                          reasoning: str, target_price: float = None, 
                          stop_loss: float = None) -> str:
        """Add a new AI recommendation"""
        recommendation_id = f"{symbol}_{action}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        recommendation = Recommendation(
            recommendation_id=recommendation_id,
            symbol=symbol,
            action=action,
            confidence=confidence,
            reasoning=reasoning,
            target_price=target_price,
            stop_loss=stop_loss,
            timestamp=datetime.now()
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO recommendations 
                (recommendation_id, symbol, action, confidence, reasoning, 
                 target_price, stop_loss, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                recommendation.recommendation_id,
                recommendation.symbol,
                recommendation.action,
                recommendation.confidence,
                recommendation.reasoning,
                recommendation.target_price,
                recommendation.stop_loss,
                recommendation.timestamp.isoformat()
            ))
            conn.commit()
        
        self.logger.info(f"Added recommendation: {action} {symbol} (confidence: {confidence}%)")
        return recommendation_id
    
    def execute_transaction(self, symbol: str, action: str, quantity: float, 
                           price: float, commission: float = 0, 
                           recommendation_id: str = None, notes: str = None) -> str:
        """Execute a buy/sell transaction"""
        transaction_id = f"{action}_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate total cost (including commission)
        if action.upper() == "BUY":
            total_cost = (quantity * price) + commission
        else:  # SELL
            total_cost = (quantity * price) - commission
        
        transaction = Transaction(
            transaction_id=transaction_id,
            symbol=symbol,
            action=action.upper(),
            quantity=quantity,
            price=price,
            total_cost=total_cost,
            commission=commission,
            timestamp=datetime.now(),
            recommendation_id=recommendation_id,
            notes=notes
        )
        
        # Save transaction
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO transactions 
                (transaction_id, symbol, action, quantity, price, total_cost, 
                 commission, timestamp, recommendation_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                transaction.transaction_id,
                transaction.symbol,
                transaction.action,
                transaction.quantity,
                transaction.price,
                transaction.total_cost,
                transaction.commission,
                transaction.timestamp.isoformat(),
                transaction.recommendation_id,
                transaction.notes
            ))
            
            # Update position
            self._update_position(conn, symbol, action, quantity, price)
            
            # Mark recommendation as executed if provided
            if recommendation_id:
                conn.execute("""
                    UPDATE recommendations 
                    SET executed = 1, execution_price = ?, execution_date = ?
                    WHERE recommendation_id = ?
                """, (price, transaction.timestamp.isoformat(), recommendation_id))
            
            conn.commit()
        
        # Clear cache
        self._clear_cache()
        
        self.logger.info(f"Executed: {action} {quantity} shares of {symbol} at ${price:.2f}")
        return transaction_id
    
    def _update_position(self, conn, symbol: str, action: str, quantity: float, price: float):
        """Update position after transaction"""
        # Get current position
        cursor = conn.execute("SELECT * FROM positions WHERE symbol = ?", (symbol,))
        current_position = cursor.fetchone()
        
        if action.upper() == "BUY":
            if current_position:
                # Update existing position
                current_qty, current_avg_cost = current_position[1], current_position[2]
                total_cost = (current_qty * current_avg_cost) + (quantity * price)
                new_quantity = current_qty + quantity
                new_avg_cost = total_cost / new_quantity
                
                conn.execute("""
                    UPDATE positions 
                    SET quantity = ?, avg_cost = ?, last_updated = ?
                    WHERE symbol = ?
                """, (new_quantity, new_avg_cost, datetime.now().isoformat(), symbol))
            else:
                # Create new position
                conn.execute("""
                    INSERT INTO positions (symbol, quantity, avg_cost, entry_date, last_updated)
                    VALUES (?, ?, ?, ?, ?)
                """, (symbol, quantity, price, datetime.now().isoformat(), datetime.now().isoformat()))
        
        elif action.upper() == "SELL":
            if current_position:
                current_qty = current_position[1]
                new_quantity = current_qty - quantity
                
                if new_quantity <= 0:
                    # Close position
                    conn.execute("DELETE FROM positions WHERE symbol = ?", (symbol,))
                else:
                    # Reduce position (keep same avg_cost)
                    conn.execute("""
                        UPDATE positions 
                        SET quantity = ?, last_updated = ?
                        WHERE symbol = ?
                    """, (new_quantity, datetime.now().isoformat(), symbol))
    
    def get_positions(self, current_prices: Dict[str, float]) -> List[Position]:
        """Get all current positions with current market values"""
        # Check cache
        if (datetime.now() < self._cache_expiry and 
            self._positions_cache and 
            all(symbol in current_prices for symbol in self._positions_cache.keys())):
            # Update prices in cached positions
            positions = []
            for symbol, position in self._positions_cache.items():
                if symbol in current_prices:
                    current_price = current_prices[symbol]
                    market_value = position.quantity * current_price
                    unrealized_pnl = market_value - (position.quantity * position.avg_cost)
                    unrealized_pnl_pct = (unrealized_pnl / (position.quantity * position.avg_cost)) * 100
                    
                    updated_position = Position(
                        symbol=position.symbol,
                        quantity=position.quantity,
                        avg_cost=position.avg_cost,
                        current_price=current_price,
                        market_value=market_value,
                        unrealized_pnl=unrealized_pnl,
                        unrealized_pnl_pct=unrealized_pnl_pct,
                        entry_date=position.entry_date,
                        last_updated=datetime.now()
                    )
                    positions.append(updated_position)
            return positions
        
        # Fetch from database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM positions")
            positions = []
            
            for row in cursor.fetchall():
                symbol, quantity, avg_cost, entry_date, last_updated = row
                
                current_price = current_prices.get(symbol, avg_cost)  # Fallback to avg_cost
                market_value = quantity * current_price
                unrealized_pnl = market_value - (quantity * avg_cost)
                unrealized_pnl_pct = (unrealized_pnl / (quantity * avg_cost)) * 100 if quantity * avg_cost > 0 else 0
                
                position = Position(
                    symbol=symbol,
                    quantity=quantity,
                    avg_cost=avg_cost,
                    current_price=current_price,
                    market_value=market_value,
                    unrealized_pnl=unrealized_pnl,
                    unrealized_pnl_pct=unrealized_pnl_pct,
                    entry_date=datetime.fromisoformat(entry_date),
                    last_updated=datetime.fromisoformat(last_updated)
                )
                positions.append(position)
                self._positions_cache[symbol] = position
        
        # Update cache expiry (cache for 5 minutes)
        self._cache_expiry = datetime.now() + timedelta(minutes=5)
        
        return positions
    
    def get_portfolio_summary(self, current_prices: Dict[str, float], cash_balance: float = 0) -> Dict[str, Any]:
        """Get comprehensive portfolio summary"""
        positions = self.get_positions(current_prices)
        
        # Calculate totals
        total_positions_value = sum(pos.market_value for pos in positions)
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in positions)
        total_portfolio_value = total_positions_value + cash_balance
        
        # Get recent performance (daily and weekly for trading model)
        daily_return = self._calculate_daily_return(total_portfolio_value)
        weekly_return = self._calculate_weekly_return(total_portfolio_value)
        
        # Get recommendation statistics
        recommendation_stats = self._get_recommendation_stats()
        
        return {
            'total_portfolio_value': total_portfolio_value,
            'cash_balance': cash_balance,
            'positions_value': total_positions_value,
            'total_unrealized_pnl': total_unrealized_pnl,
            'unrealized_pnl_pct': (total_unrealized_pnl / (total_positions_value - total_unrealized_pnl)) * 100 if total_positions_value > total_unrealized_pnl else 0,
            'daily_return': daily_return,
            'weekly_return': weekly_return,
            'position_count': len(positions),
            'largest_position': max(positions, key=lambda p: p.market_value) if positions else None,
            'largest_gainer': max(positions, key=lambda p: p.unrealized_pnl_pct) if positions else None,
            'largest_loser': min(positions, key=lambda p: p.unrealized_pnl_pct) if positions else None,
            'recommendation_stats': recommendation_stats,
            'last_updated': datetime.now()
        }
    
    def _calculate_daily_return(self, current_value: float) -> float:
        """Calculate daily return percentage"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT total_value FROM portfolio_snapshots 
                    ORDER BY timestamp DESC LIMIT 2
                """)
                snapshots = cursor.fetchall()
                
                if len(snapshots) >= 2:
                    yesterday_value = snapshots[1][0]
                    return ((current_value - yesterday_value) / yesterday_value) * 100
                return 0.0
        except:
            return 0.0
    
    def _calculate_weekly_return(self, current_value: float) -> float:
        """Calculate weekly return percentage (for weekly trading model)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get snapshot from 7 days ago
                week_ago = datetime.now() - timedelta(days=7)
                cursor = conn.execute("""
                    SELECT total_value FROM portfolio_snapshots 
                    WHERE timestamp <= ? 
                    ORDER BY timestamp DESC LIMIT 1
                """, (week_ago.isoformat(),))
                
                result = cursor.fetchone()
                if result:
                    week_ago_value = result[0]
                    return ((current_value - week_ago_value) / week_ago_value) * 100
                return 0.0
        except:
            return 0.0
    
    def get_weekly_performance_summary(self) -> Dict[str, Any]:
        """Get weekly performance summary for weekly trading model"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get weekly snapshots (every 7 days)
                cursor = conn.execute("""
                    SELECT total_value, timestamp, positions_value, cash_balance
                    FROM portfolio_snapshots 
                    WHERE DATE(timestamp) = DATE(timestamp, 'weekday 1', '-7 days')
                    OR timestamp >= DATE('now', '-8 days')
                    ORDER BY timestamp DESC
                    LIMIT 8
                """)
                
                weekly_data = cursor.fetchall()
                
                if len(weekly_data) < 2:
                    return {'insufficient_data': True}
                
                # Calculate weekly metrics
                current_value = weekly_data[0][0]
                last_week_value = weekly_data[1][0] if len(weekly_data) > 1 else weekly_data[0][0]
                
                weekly_return = ((current_value - last_week_value) / last_week_value) * 100 if last_week_value > 0 else 0
                
                # Weekly volatility
                values = [row[0] for row in weekly_data]
                if len(values) > 2:
                    weekly_returns = [((values[i] - values[i+1]) / values[i+1]) * 100 for i in range(len(values)-1)]
                    weekly_volatility = np.std(weekly_returns) if len(weekly_returns) > 1 else 0
                else:
                    weekly_volatility = 0
                
                return {
                    'current_value': current_value,
                    'last_week_value': last_week_value,
                    'weekly_return_pct': weekly_return,
                    'weekly_volatility_pct': weekly_volatility,
                    'weeks_tracked': len(weekly_data),
                    'best_week': max(weekly_returns) if 'weekly_returns' in locals() and weekly_returns else 0,
                    'worst_week': min(weekly_returns) if 'weekly_returns' in locals() and weekly_returns else 0
                }
                
        except Exception as e:
            self.logger.error(f"Error calculating weekly performance: {e}")
            return {'error': str(e)}
    
    def _get_recommendation_stats(self) -> Dict[str, Any]:
        """Get recommendation performance statistics"""
        with sqlite3.connect(self.db_path) as conn:
            # Total recommendations
            cursor = conn.execute("SELECT COUNT(*) FROM recommendations")
            total_recommendations = cursor.fetchone()[0]
            
            # Executed recommendations
            cursor = conn.execute("SELECT COUNT(*) FROM recommendations WHERE executed = 1")
            executed_recommendations = cursor.fetchone()[0]
            
            # Successful recommendations (placeholder - would need outcome scoring)
            cursor = conn.execute("SELECT COUNT(*) FROM recommendations WHERE outcome_score > 0")
            successful_recommendations = cursor.fetchone()[0]
            
            execution_rate = (executed_recommendations / total_recommendations * 100) if total_recommendations > 0 else 0
            success_rate = (successful_recommendations / executed_recommendations * 100) if executed_recommendations > 0 else 0
            
            return {
                'total_recommendations': total_recommendations,
                'executed_recommendations': executed_recommendations,
                'execution_rate': execution_rate,
                'success_rate': success_rate,
                'successful_recommendations': successful_recommendations
            }
    
    def save_portfolio_snapshot(self, current_prices: Dict[str, float], cash_balance: float = 0):
        """Save current portfolio state for historical tracking"""
        positions = self.get_positions(current_prices)
        summary = self.get_portfolio_summary(current_prices, cash_balance)
        
        snapshot_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Serialize positions for storage
        positions_json = json.dumps([asdict(pos) for pos in positions], default=str)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO portfolio_snapshots 
                (snapshot_id, timestamp, total_value, cash_balance, positions_value, 
                 total_pnl, daily_return, positions_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                snapshot_id,
                datetime.now().isoformat(),
                summary['total_portfolio_value'],
                cash_balance,
                summary['positions_value'],
                summary['total_unrealized_pnl'],
                summary['daily_return'],
                positions_json
            ))
            conn.commit()
    
    def get_transactions_history(self, symbol: str = None, days: int = 30) -> List[Transaction]:
        """Get transaction history"""
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT * FROM transactions 
                WHERE timestamp > ? 
            """
            params = [datetime.now() - timedelta(days=days)]
            
            if symbol:
                query += " AND symbol = ?"
                params.append(symbol)
            
            query += " ORDER BY timestamp DESC"
            
            cursor = conn.execute(query, params)
            transactions = []
            
            for row in cursor.fetchall():
                transaction = Transaction(
                    transaction_id=row[0],
                    symbol=row[1],
                    action=row[2],
                    quantity=row[3],
                    price=row[4],
                    total_cost=row[5],
                    commission=row[6],
                    timestamp=datetime.fromisoformat(row[7]),
                    recommendation_id=row[8],
                    notes=row[9]
                )
                transactions.append(transaction)
            
            return transactions
    
    def _clear_cache(self):
        """Clear positions cache"""
        self._positions_cache.clear()
        self._cache_expiry = datetime.now()
    
    def get_performance_metrics(self, days: int = 30) -> Dict[str, float]:
        """Calculate comprehensive performance metrics"""
        # This would include Sharpe ratio, max drawdown, etc.
        # Placeholder for now - can be expanded based on needs
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT total_value, timestamp FROM portfolio_snapshots 
                WHERE timestamp > ? 
                ORDER BY timestamp
            """, [datetime.now() - timedelta(days=days)])
            
            snapshots = cursor.fetchall()
            
            if len(snapshots) < 2:
                return {'insufficient_data': True}
            
            values = [s[0] for s in snapshots]
            returns = [(values[i] - values[i-1]) / values[i-1] for i in range(1, len(values))]
            
            if not returns:
                return {'insufficient_data': True}
            
            total_return = (values[-1] - values[0]) / values[0] * 100
            avg_daily_return = np.mean(returns) * 100
            volatility = np.std(returns) * 100
            
            # Simple Sharpe ratio approximation (assuming 2% risk-free rate)
            excess_returns = [r - 0.02/365 for r in returns]
            sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252) if np.std(excess_returns) > 0 else 0
            
            # Max drawdown
            peak = values[0]
            max_drawdown = 0
            for value in values:
                if value > peak:
                    peak = value
                else:
                    drawdown = (peak - value) / peak
                    max_drawdown = max(max_drawdown, drawdown)
            
            return {
                'total_return_pct': total_return,
                'avg_daily_return_pct': avg_daily_return,
                'volatility_pct': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown_pct': max_drawdown * 100,
                'periods': len(snapshots)
            }

# Test function
if __name__ == "__main__":
    # Example usage
    tracker = PortfolioTracker("data/test_portfolio.db")
    
    # Add a recommendation
    rec_id = tracker.add_recommendation("AAPL", "BUY", 75.0, "Strong technical indicators")
    
    # Execute a transaction
    tracker.execute_transaction("AAPL", "BUY", 100, 150.0, 1.0, rec_id)
    
    # Get portfolio summary
    current_prices = {"AAPL": 155.0}
    summary = tracker.get_portfolio_summary(current_prices, 10000)
    
    print("Portfolio Summary:")
    for key, value in summary.items():
        if key != 'recommendation_stats':
            print(f"  {key}: {value}")
    
    print("\nRecommendation Stats:")
    for key, value in summary['recommendation_stats'].items():
        print(f"  {key}: {value}")
