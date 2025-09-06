#!/usr/bin/env python3
"""
Portfolio UI Components
Streamlit components for manual portfolio tracking - user enters real positions
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Any

def display_portfolio_summary(portfolio_status: Dict[str, Any]):
    """Display portfolio summary cards"""
    
    st.subheader("📊 Portfolio Overview")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Value", 
            f"${portfolio_status['total_portfolio_value']:,.2f}",
            delta=f"{portfolio_status.get('weekly_return', 0):+.2f}% (week)" if portfolio_status.get('weekly_return') else None
        )
    
    with col2:
        st.metric(
            "Cash Balance", 
            f"${portfolio_status['cash_balance']:,.2f}",
            delta=f"{portfolio_status.get('cash_percentage', 0):.1f}% of portfolio"
        )
    
    with col3:
        st.metric(
            "Unrealized P&L", 
            f"${portfolio_status.get('total_unrealized_pnl', 0):,.2f}",
            delta=f"{portfolio_status.get('unrealized_pnl_pct', 0):.2f}%"
        )
    
    with col4:
        if portfolio_status.get('testing_mode'):
            st.metric(
                "Testing Days", 
                f"{portfolio_status.get('testing_duration_days', 0)}",
                "📊 Test Mode"
            )
        else:
            st.metric(
                "Positions", 
                f"{portfolio_status.get('position_count', 0)}",
                "🏢 Holdings"
            )

def display_positions_table(positions: List[Any]):
    """Display current positions in a table"""
    
    if not positions:
        st.info("📝 No current positions")
        return
    
    st.subheader("🏢 Current Positions")
    
    # Convert positions to DataFrame
    positions_data = []
    for pos in positions:
        positions_data.append({
            'Symbol': pos.symbol,
            'Quantity': f"{pos.quantity:,.0f}",
            'Avg Cost': f"${pos.avg_cost:.2f}",
            'Current Price': f"${pos.current_price:.2f}",
            'Market Value': f"${pos.market_value:,.2f}",
            'Unrealized P&L': f"${pos.unrealized_pnl:,.2f}",
            'P&L %': f"{pos.unrealized_pnl_pct:.2f}%",
            'Entry Date': pos.entry_date.strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(positions_data)
    
    # Color code P&L
    def color_pnl(val):
        if 'P&L %' in val.name:
            try:
                pct = float(val.replace('%', ''))
                if pct > 0:
                    return ['background-color: rgba(0, 255, 0, 0.1)'] * len(val)
                elif pct < 0:
                    return ['background-color: rgba(255, 0, 0, 0.1)'] * len(val)
            except:
                pass
        return [''] * len(val)
    
    # Display styled table
    styled_df = df.style.apply(color_pnl, axis=0)
    st.dataframe(styled_df, use_container_width=True)

def display_portfolio_allocation(portfolio_status: Dict[str, Any]):
    """Display portfolio allocation pie chart"""
    
    allocations = portfolio_status.get('position_allocations', {})
    cash_pct = portfolio_status.get('cash_percentage', 0)
    
    if not allocations and cash_pct == 100:
        st.info("💰 Portfolio is 100% cash")
        return
    
    st.subheader("🥧 Portfolio Allocation")
    
    # Prepare data for pie chart
    labels = list(allocations.keys()) + ['Cash']
    values = list(allocations.values()) + [cash_pct]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        hole=0.3,
        hovertemplate="<b>%{label}</b><br>%{value:.1f}%<br>%{text}<extra></extra>",
        text=[f"${portfolio_status['total_portfolio_value'] * v / 100:,.0f}" for v in values]
    )])
    
    fig.update_layout(
        title="Portfolio Allocation",
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_recommendations_table(recommendations: List[Dict[str, Any]]):
    """Display recent recommendations"""
    
    if not recommendations:
        st.info("📋 No recent recommendations")
        return
    
    st.subheader("🎯 Recent Recommendations")
    
    # Convert to DataFrame
    rec_data = []
    for rec in recommendations:
        rec_data.append({
            'Symbol': rec.get('symbol', 'N/A'),
            'Action': rec.get('action', 'N/A'),
            'Confidence': f"{rec.get('confidence', 0):.0f}%",
            'Current Price': f"${rec.get('current_price', 0):.2f}",
            'Reasoning': rec.get('reasoning', 'N/A')[:50] + "..." if len(rec.get('reasoning', '')) > 50 else rec.get('reasoning', 'N/A'),
            'Timestamp': rec.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M')
        })
    
    df = pd.DataFrame(rec_data)
    
    # Color code actions
    def color_actions(val):
        if val.name == 'Action':
            colors = []
            for action in val:
                if action == 'BUY':
                    colors.append('background-color: rgba(0, 255, 0, 0.2)')
                elif action == 'SELL':
                    colors.append('background-color: rgba(255, 0, 0, 0.2)')
                else:  # HOLD
                    colors.append('background-color: rgba(255, 255, 0, 0.2)')
            return colors
        return [''] * len(val)
    
    styled_df = df.style.apply(color_actions, axis=0)
    st.dataframe(styled_df, use_container_width=True)

def display_performance_chart(performance_data: List[Dict[str, Any]]):
    """Display portfolio performance over time"""
    
    if not performance_data or len(performance_data) < 2:
        st.info("📈 Insufficient data for performance chart")
        return
    
    st.subheader("📈 Portfolio Performance")
    
    # Convert to DataFrame
    df = pd.DataFrame(performance_data)
    df['Date'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('Date')
    
    # Calculate daily returns
    df['Daily_Return'] = df['total_value'].pct_change() * 100
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Portfolio Value', 'Daily Returns %'),
        row_heights=[0.7, 0.3]
    )
    
    # Portfolio value line
    fig.add_trace(
        go.Scatter(
            x=df['Date'], 
            y=df['total_value'],
            mode='lines',
            name='Portfolio Value',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )
    
    # Daily returns bar chart
    colors = ['green' if x > 0 else 'red' for x in df['Daily_Return'].fillna(0)]
    fig.add_trace(
        go.Bar(
            x=df['Date'], 
            y=df['Daily_Return'].fillna(0),
            name='Daily Return %',
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        title_text="Portfolio Performance Over Time",
        showlegend=True
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Value ($)", row=1, col=1)
    fig.update_yaxes(title_text="Return (%)", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

def display_testing_report(report: Dict[str, Any]):
    """Display comprehensive testing report"""
    
    st.subheader("🧪 Testing Report")
    
    if 'error' in report:
        st.error(f"Error generating report: {report['error']}")
        return
    
    # Testing overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Testing Duration", 
            f"{report.get('testing_duration_days', 0)} days",
            "📅 Period"
        )
    
    with col2:
        st.metric(
            "Total Return", 
            f"{report.get('total_return_pct', 0):.2f}%",
            "💰 Performance"
        )
    
    with col3:
        st.metric(
            "Recommendations", 
            f"{report.get('total_recommendations', 0)}",
            f"{report.get('execution_rate_pct', 0):.1f}% executed"
        )
    
    # Recommendation breakdown
    st.subheader("📊 Recommendation Breakdown")
    
    rec_breakdown = report.get('recommendations_by_action', {})
    if rec_breakdown:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("BUY Signals", rec_breakdown.get('BUY', 0), "🟢")
        with col2:
            st.metric("SELL Signals", rec_breakdown.get('SELL', 0), "🔴")
        with col3:
            st.metric("HOLD Signals", rec_breakdown.get('HOLD', 0), "🟡")
    
    # Performance metrics
    perf_metrics = report.get('performance_metrics', {})
    if perf_metrics and not perf_metrics.get('insufficient_data'):
        st.subheader("📈 Performance Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Sharpe Ratio", f"{perf_metrics.get('sharpe_ratio', 0):.2f}")
            st.metric("Avg Daily Return", f"{perf_metrics.get('avg_daily_return_pct', 0):.2f}%")
        
        with col2:
            st.metric("Volatility", f"{perf_metrics.get('volatility_pct', 0):.2f}%")
            st.metric("Max Drawdown", f"{perf_metrics.get('max_drawdown_pct', 0):.2f}%")
    
    # System accuracy assessment
    st.subheader("🎯 System Accuracy Assessment")
    
    avg_confidence = report.get('avg_confidence', 0)
    execution_rate = report.get('execution_rate_pct', 0)
    
    # Simple scoring system
    confidence_score = "High" if avg_confidence > 70 else "Medium" if avg_confidence > 50 else "Low"
    execution_score = "High" if execution_rate > 60 else "Medium" if execution_rate > 30 else "Low"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Avg Confidence", f"{avg_confidence:.1f}%", confidence_score)
    with col2:
        st.metric("Execution Rate", f"{execution_rate:.1f}%", execution_score)
    
    # Overall assessment
    st.subheader("📋 Overall Assessment")
    
    total_return = report.get('total_return_pct', 0)
    
    if total_return > 5:
        st.success("🎉 System showing strong performance!")
    elif total_return > 0:
        st.info("📈 System showing positive performance")
    elif total_return > -5:
        st.warning("⚠️ System showing neutral performance")
    else:
        st.error("📉 System needs adjustment")
    
    # Display detailed metrics in expander
    with st.expander("📊 Detailed Metrics"):
        st.json(report)

def display_transaction_history(transactions: List[Any], days: int = 30):
    """Display transaction history"""
    
    if not transactions:
        st.info("📜 No recent transactions")
        return
    
    st.subheader(f"📜 Transaction History (Last {days} days)")
    
    # Convert to DataFrame
    trans_data = []
    for trans in transactions:
        trans_data.append({
            'Date': trans.timestamp.strftime('%Y-%m-%d %H:%M'),
            'Symbol': trans.symbol,
            'Action': trans.action,
            'Quantity': f"{trans.quantity:,.0f}",
            'Price': f"${trans.price:.2f}",
            'Total': f"${abs(trans.total_cost):,.2f}",
            'Commission': f"${trans.commission:.2f}",
            'Notes': trans.notes[:30] + "..." if trans.notes and len(trans.notes) > 30 else trans.notes or "N/A"
        })
    
    df = pd.DataFrame(trans_data)
    
    # Color code by action
    def color_transactions(val):
        if val.name == 'Action':
            colors = []
            for action in val:
                if action == 'BUY':
                    colors.append('background-color: rgba(0, 255, 0, 0.1)')
                else:  # SELL
                    colors.append('background-color: rgba(255, 0, 0, 0.1)')
            return colors
        return [''] * len(val)
    
    styled_df = df.style.apply(color_transactions, axis=0)
    st.dataframe(styled_df, use_container_width=True)

def display_risk_metrics(portfolio_status: Dict[str, Any]):
    """Display portfolio risk metrics"""
    
    risk_metrics = portfolio_status.get('risk_metrics', {})
    
    if not risk_metrics:
        st.info("⚠️ No risk metrics available")
        return
    
    st.subheader("⚠️ Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        concentration_risk = risk_metrics.get('concentration_risk', 0)
        if concentration_risk > 2:
            st.error(f"High Concentration Risk: {concentration_risk:.1f}")
        elif concentration_risk > 1:
            st.warning(f"Medium Concentration Risk: {concentration_risk:.1f}")
        else:
            st.success(f"Low Concentration Risk: {concentration_risk:.1f}")
    
    with col2:
        largest_position = risk_metrics.get('largest_position_pct', 0)
        st.metric("Largest Position", f"{largest_position:.1f}%")
    
    with col3:
        position_count = risk_metrics.get('position_count', 0)
        diversification = "High" if position_count > 10 else "Medium" if position_count > 5 else "Low"
        st.metric("Diversification", diversification, f"{position_count} positions")

# Utility functions for Streamlit integration
def portfolio_sidebar_controls():
    """Create sidebar controls for manual portfolio management"""
    
    st.sidebar.subheader("💼 Manual Portfolio Controls")
    
    # Cash balance input (user enters actual balance)
    cash_balance = st.sidebar.number_input(
        "💰 Actual Cash Balance", 
        min_value=0.0, 
        value=50000.0, 
        step=1000.0,
        format="%.2f",
        help="Enter your real cash balance from brokerage account"
    )
    
    # Risk tolerance for TA recommendations
    risk_tolerance = st.sidebar.selectbox(
        "⚖️ Risk Tolerance",
        options=['conservative', 'moderate', 'aggressive'],
        index=1,
        help="Affects TA recommendation thresholds for your holdings"
    )
    
    # Manual entry buttons
    st.sidebar.subheader("📝 Manual Entry")
    
    add_position = st.sidebar.button("➕ Add Position", help="Manually add a stock position")
    record_transaction = st.sidebar.button("📊 Record Transaction", help="Log a completed trade")
    update_cash = st.sidebar.button("💰 Update Cash", help="Update cash balance")
    
    return {
        'cash_balance': cash_balance,
        'risk_tolerance': risk_tolerance,
        'add_position': add_position,
        'record_transaction': record_transaction,
        'update_cash': update_cash
    }

def display_manual_entry_forms():
    """Display forms for manual data entry"""
    
    st.subheader("📝 Manual Entry Forms")
    
    tab1, tab2, tab3 = st.tabs(["Add Position", "Record Transaction", "Update Cash"])
    
    with tab1:
        st.write("**Add New Position**")
        st.info("Enter a position you actually own in your brokerage account")
        
        col1, col2 = st.columns(2)
        with col1:
            symbol = st.text_input("Stock Symbol", placeholder="AAPL", help="Stock ticker symbol")
            quantity = st.number_input("Quantity", min_value=1, value=100, help="Number of shares owned")
        
        with col2:
            purchase_price = st.number_input("Purchase Price ($)", min_value=0.01, value=150.00, format="%.2f")
            purchase_date = st.date_input("Purchase Date", help="When you bought this position")
        
        commission = st.number_input("Commission ($)", min_value=0.0, value=1.00, format="%.2f")
        notes = st.text_area("Notes (optional)", placeholder="Initial position from portfolio transfer")
        
        if st.button("Add Position", type="primary"):
            st.success(f"Position added: {quantity} shares of {symbol} at ${purchase_price}")
            st.rerun()
    
    with tab2:
        st.write("**Record Completed Transaction**")
        st.info("Log a trade you already completed in your brokerage account")
        
        col1, col2 = st.columns(2)
        with col1:
            trans_symbol = st.text_input("Symbol", placeholder="AAPL", key="trans_symbol")
            action = st.selectbox("Action", ["BUY", "SELL"])
            trans_quantity = st.number_input("Quantity", min_value=1, value=50, key="trans_quantity")
        
        with col2:
            execution_price = st.number_input("Execution Price ($)", min_value=0.01, value=155.00, format="%.2f")
            execution_date = st.date_input("Execution Date", key="exec_date")
        
        trans_commission = st.number_input("Commission ($)", min_value=0.0, value=1.00, format="%.2f", key="trans_commission")
        trans_notes = st.text_area("Notes (optional)", placeholder="Followed TA recommendation", key="trans_notes")
        
        if st.button("Record Transaction", type="primary"):
            st.success(f"Transaction recorded: {action} {trans_quantity} shares of {trans_symbol} at ${execution_price}")
            st.rerun()
    
    with tab3:
        st.write("**Update Cash Balance**")
        st.info("Update your cash balance to match your brokerage account")
        
        new_cash_balance = st.number_input(
            "New Cash Balance ($)", 
            min_value=0.0, 
            value=50000.0, 
            format="%.2f"
        )
        
        cash_notes = st.text_area(
            "Reason for change", 
            placeholder="Deposited $10,000, received $500 dividend from MSFT"
        )
        
        if st.button("Update Cash Balance", type="primary"):
            st.success(f"Cash balance updated to ${new_cash_balance:,.2f}")
            st.rerun()

def display_ta_recommendations_for_holdings(holdings_analysis: Dict[str, Any]):
    """Display TA recommendations specifically for owned stocks"""
    
    if not holdings_analysis or not holdings_analysis.get('holdings_analysis'):
        st.info("📋 No holdings to analyze")
        return
    
    st.subheader("🎯 TA Recommendations for Your Holdings")
    st.write("Technical analysis recommendations for stocks you actually own")
    
    # Summary cards
    summary = holdings_analysis['summary']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Holdings", summary['total_holdings'])
    with col2:
        st.metric("BUY Signals", summary['buy_signals'], "🟢")
    with col3:
        st.metric("SELL Signals", summary['sell_signals'], "🔴") 
    with col4:
        st.metric("HOLD Signals", summary['hold_signals'], "🟡")
    
    # Detailed recommendations
    for symbol, analysis in holdings_analysis['holdings_analysis'].items():
        if analysis.get('success'):
            with st.expander(f"{symbol} - {analysis['action']} ({analysis['confidence']}% confidence)"):
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.write("**Position Details:**")
                    holding = analysis['holding_details']
                    st.write(f"• Quantity: {holding['quantity']:,.0f} shares")
                    st.write(f"• Avg Cost: ${holding['avg_cost']:.2f}")
                    st.write(f"• Current Price: ${analysis['current_price']:.2f}")
                    st.write(f"• Market Value: ${holding['market_value']:,.2f}")
                    st.write(f"• P&L: ${holding['unrealized_pnl']:,.2f} ({holding['unrealized_pnl_pct']:+.1f}%)")
                
                with col2:
                    st.write("**Technical Analysis:**")
                    tech = analysis['technical_summary']
                    st.write(f"• RSI: {tech['rsi']:.1f}")
                    st.write(f"• SMA 20: ${tech['sma_20']:.2f}")
                    st.write(f"• Trend: {tech['trend'].title()}")
                    st.write(f"• BB Position: {tech['bb_position'].title()}")
                
                # Recommendation and advice
                if analysis['action'] == 'BUY':
                    st.success(f"**Recommendation:** {analysis['action']} ({analysis['confidence']}%)")
                elif analysis['action'] == 'SELL':
                    st.error(f"**Recommendation:** {analysis['action']} ({analysis['confidence']}%)")
                else:
                    st.warning(f"**Recommendation:** {analysis['action']} ({analysis['confidence']}%)")
                
                st.info(f"**Position Advice:** {analysis['position_advice']}")
                st.write(f"**Reasoning:** {analysis['reasoning']}")
        
        else:
            st.error(f"{symbol}: Analysis failed - {analysis.get('error', 'Unknown error')}")
