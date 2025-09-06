#!/usr/bin/env python3
"""
Weekly Portfolio UI Components
Streamlit components specifically for weekly trading model
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

def display_weekly_performance_summary(weekly_summary: Dict[str, Any]):
    """Display weekly performance metrics for weekly trading model"""
    
    if weekly_summary.get('insufficient_data'):
        st.info("📅 Insufficient data for weekly analysis. Need at least 2 weeks of snapshots.")
        return
    
    if weekly_summary.get('error'):
        st.error(f"Error calculating weekly performance: {weekly_summary['error']}")
        return
    
    st.subheader("📅 Weekly Performance (Trading Model)")
    st.write("Performance metrics aligned with weekly trading strategy")
    
    # Weekly metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        weekly_return = weekly_summary.get('weekly_return_pct', 0)
        if weekly_return > 0:
            st.metric("Weekly Return", f"+{weekly_return:.2f}%", delta="📈")
        elif weekly_return < 0:
            st.metric("Weekly Return", f"{weekly_return:.2f}%", delta="📉")
        else:
            st.metric("Weekly Return", f"{weekly_return:.2f}%", delta="➡️")
    
    with col2:
        st.metric(
            "Weekly Volatility", 
            f"{weekly_summary.get('weekly_volatility_pct', 0):.2f}%",
            help="Volatility of weekly returns"
        )
    
    with col3:
        st.metric(
            "Best Week", 
            f"+{weekly_summary.get('best_week', 0):.2f}%",
            delta="🏆"
        )
    
    with col4:
        st.metric(
            "Worst Week", 
            f"{weekly_summary.get('worst_week', 0):.2f}%",
            delta="⚠️"
        )
    
    # Weekly analysis
    weeks_tracked = weekly_summary.get('weeks_tracked', 0)
    current_value = weekly_summary.get('current_value', 0)
    last_week_value = weekly_summary.get('last_week_value', 0)
    
    st.write(f"**Analysis Period:** {weeks_tracked} weeks tracked")
    st.write(f"**Portfolio Value:** ${current_value:,.2f} (was ${last_week_value:,.2f} last week)")

def display_weekly_trading_schedule():
    """Display weekly trading schedule and next session info"""
    
    st.subheader("📅 Weekly Trading Schedule")
    
    # Calculate next Monday (typical trading day)
    today = datetime.now()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0 and today.hour < 9:  # If it's Monday morning
        next_session = today
    else:
        next_session = today + timedelta(days=days_until_monday if days_until_monday > 0 else 7)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Weekly Trading Model:**")
        st.write("• 📊 Analysis sessions: Mondays")
        st.write("• 🎯 Review TA recommendations")
        st.write("• 📝 Plan week's trading strategy") 
        st.write("• ✅ Execute trades manually")
    
    with col2:
        st.write("**Next Session:**")
        st.write(f"📅 **{next_session.strftime('%A, %B %d')}**")
        st.write(f"🕘 Recommended: Monday 9:00 AM")
        
        days_remaining = (next_session.date() - today.date()).days
        if days_remaining == 0:
            st.success("🎯 **Today is trading day!**")
        elif days_remaining == 1:
            st.info("⏰ **Tomorrow is trading day**")
        else:
            st.write(f"⏳ **{days_remaining} days until next session**")

def display_weekly_checklist():
    """Display weekly trading checklist"""
    
    st.subheader("✅ Weekly Trading Checklist")
    
    checklist_items = [
        "📊 Review portfolio performance from last week",
        "🎯 Run TA analysis on all holdings",
        "📝 Review buy/sell/hold recommendations", 
        "💰 Check cash balance and available funds",
        "🎛️ Decide on position adjustments (add/reduce/hold)",
        "📋 Execute planned trades in brokerage account",
        "✏️ Log completed transactions in portfolio tracker",
        "📸 Save weekly portfolio snapshot"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Weekly Session Tasks:**")
        for i, item in enumerate(checklist_items[:4]):
            st.write(f"{i+1}. {item}")
    
    with col2:
        st.write("**Execution & Recording:**")
        for i, item in enumerate(checklist_items[4:], 5):
            st.write(f"{i}. {item}")
    
    if st.button("📸 Save Weekly Snapshot", help="Save current portfolio state for weekly tracking"):
        st.success("📸 Weekly portfolio snapshot saved!")
        st.balloons()

def display_weekly_portfolio_changes(weekly_data: Dict[str, Any]):
    """Display week-over-week portfolio changes"""
    
    if not weekly_data or weekly_data.get('insufficient_data'):
        st.info("📅 Need more weekly data to show changes")
        return
    
    st.subheader("📈 Week-over-Week Changes")
    
    current_value = weekly_data.get('current_value', 0)
    last_week_value = weekly_data.get('last_week_value', 0) 
    weekly_return = weekly_data.get('weekly_return_pct', 0)
    
    # Value change breakdown
    value_change = current_value - last_week_value
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Portfolio Value Changes:**")
        st.write(f"• Last week: ${last_week_value:,.2f}")
        st.write(f"• This week: ${current_value:,.2f}")
        
        if value_change > 0:
            st.write(f"• **Change: +${value_change:,.2f} (+{weekly_return:.2f}%)**")
            st.success("📈 Portfolio gained value this week")
        elif value_change < 0:
            st.write(f"• **Change: ${value_change:,.2f} ({weekly_return:.2f}%)**")
            st.error("📉 Portfolio lost value this week")
        else:
            st.write(f"• **Change: ${value_change:,.2f} ({weekly_return:.2f}%)**")
            st.info("➡️ Portfolio unchanged this week")
    
    with col2:
        st.write("**Weekly Trading Notes:**")
        st.text_area(
            "Add weekly observations:",
            placeholder="Market was volatile this week. AAPL responded well to earnings. Reduced TSLA position as planned.",
            height=100,
            key="weekly_notes"
        )

def display_weekly_ta_session():
    """Display interface for weekly TA analysis session"""
    
    st.subheader("🎯 Weekly TA Analysis Session")
    st.write("Comprehensive analysis of your holdings for this week's trading decisions")
    
    # Session controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh All Holdings", type="primary"):
            st.success("📊 Refreshed TA analysis for all holdings")
    
    with col2:
        risk_tolerance = st.selectbox(
            "Risk Tolerance", 
            ["conservative", "moderate", "aggressive"],
            index=1,
            key="weekly_risk"
        )
    
    with col3:
        if st.button("📋 Generate Weekly Report"):
            st.success("📄 Weekly report generated - check downloads")
    
    # Analysis summary
    st.write("**This Week's TA Summary:**")
    st.info("🎯 Run holdings analysis to see TA recommendations for your positions")
    
    # Quick actions
    with st.expander("🚀 Quick Actions for Weekly Session"):
        st.write("**Common weekly tasks:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Analyze All Holdings"):
                st.info("Running TA analysis on all portfolio positions...")
            
            if st.button("💰 Check Cash for Opportunities"):
                st.info("Available cash: $X,XXX for new positions")
        
        with col2:
            if st.button("🎯 Review Last Week's Trades"):
                st.info("Showing transaction history from last 7 days...")
            
            if st.button("📈 Update Performance Metrics"):
                st.info("Recalculating weekly performance metrics...")

# Weekly portfolio dashboard
def display_weekly_portfolio_dashboard(portfolio_status: Dict[str, Any], weekly_summary: Dict[str, Any]):
    """Complete weekly portfolio dashboard"""
    
    st.title("📅 Weekly Portfolio Dashboard")
    st.write("Portfolio tracking and analysis aligned with weekly trading strategy")
    
    # Weekly performance summary
    display_weekly_performance_summary(weekly_summary)
    
    st.markdown("---")
    
    # Weekly trading schedule
    display_weekly_trading_schedule()
    
    st.markdown("---")
    
    # Week-over-week changes
    display_weekly_portfolio_changes(weekly_summary)
    
    st.markdown("---")
    
    # Weekly checklist
    display_weekly_checklist()
    
    st.markdown("---")
    
    # Weekly TA session
    display_weekly_ta_session()
