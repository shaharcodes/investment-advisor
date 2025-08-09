import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Investment Advisor",
    page_icon="📈",
    layout="wide"
)

# Simple TA functions
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(com=period-1, adjust=False).mean()
    avg_loss = loss.ewm(com=period-1, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_sma(data, period=20):
    return data.rolling(window=period).mean()

def generate_recommendation(price, rsi, sma):
    signals = 0
    reasons = []
    
    if rsi < 30:
        signals += 2
        reasons.append("RSI oversold (< 30)")
    elif rsi > 70:
        signals -= 2
        reasons.append("RSI overbought (> 70)")
    
    if price > sma:
        signals += 1
        reasons.append("Price above 20-day SMA")
    else:
        signals -= 1
        reasons.append("Price below 20-day SMA")
    
    if signals > 1:
        action = "BUY"
        confidence = min(85, 60 + signals * 10)
    elif signals < -1:
        action = "SELL"
        confidence = min(85, 60 + abs(signals) * 10)
    else:
        action = "HOLD"
        confidence = 50
    
    return action, confidence, reasons

# Main app
st.title("📈 Investment Advisor Pro")
st.markdown("---")

# Sidebar
st.sidebar.title("🎯 Settings")
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=1)
investment = st.sidebar.number_input("Investment Amount ($)", value=10000, min_value=100)

if st.sidebar.button("🔍 Analyze Stock", type="primary"):
    try:
        # Fetch data
        with st.spinner(f"Fetching data for {symbol}..."):
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            info = ticker.info
        
        if not data.empty:
            latest = data.iloc[-1]
            current_price = latest['Close']
            
            # Calculate indicators
            rsi = calculate_rsi(data['Close'])
            sma20 = calculate_sma(data['Close'], 20)
            
            # Generate recommendation
            action, confidence, reasons = generate_recommendation(
                current_price, rsi.iloc[-1], sma20.iloc[-1]
            )
            
            # Display results
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"${current_price:.2f}")
            with col2:
                st.metric("RSI", f"{rsi.iloc[-1]:.1f}")
            with col3:
                st.metric("20-day SMA", f"${sma20.iloc[-1]:.2f}")
            with col4:
                market_cap = info.get('marketCap', 0)
                if market_cap > 1e9:
                    cap_str = f"${market_cap/1e9:.1f}B"
                else:
                    cap_str = f"${market_cap/1e6:.1f}M"
                st.metric("Market Cap", cap_str)
            
            # Company info
            company_name = info.get('longName', symbol)
            sector = info.get('sector', 'N/A')
            st.info(f"**{company_name}** | {sector}")
            
            # Recommendation
            if action == "BUY":
                st.success(f"🟢 Recommendation: {action} ({confidence}% confidence)")
            elif action == "SELL":
                st.error(f"🔴 Recommendation: {action} ({confidence}% confidence)")
            else:
                st.warning(f"🟡 Recommendation: {action} ({confidence}% confidence)")
            
            # Position sizing
            if action in ["BUY", "SELL"]:
                position_pct = min(15, confidence * 0.2)
                position_amount = investment * (position_pct / 100)
                shares = position_amount / current_price
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Suggested Position", f"{position_pct:.1f}%")
                with col2:
                    st.metric("Investment Amount", f"${position_amount:,.0f}")
                with col3:
                    st.metric("Estimated Shares", f"{shares:.0f}")
            
            # Reasoning
            with st.expander("📋 Analysis Details"):
                for reason in reasons:
                    st.write(f"• {reason}")
            
            # Chart
            fig = go.Figure()
            
            # Candlestick
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="Price"
            ))
            
            # SMA
            fig.add_trace(go.Scatter(
                x=data.index,
                y=sma20,
                name="SMA 20",
                line=dict(color='orange')
            ))
            
            fig.update_layout(
                title=f"{symbol} Price Chart",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # RSI Chart
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=data.index, y=rsi, name="RSI"))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            fig_rsi.update_layout(
                title="RSI Indicator",
                yaxis=dict(range=[0, 100]),
                height=300
            )
            
            st.plotly_chart(fig_rsi, use_container_width=True)
            
        else:
            st.error(f"No data found for {symbol}")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("👆 Enter a stock symbol and click 'Analyze Stock' to get started!")

# Footer
st.markdown("---")
st.markdown("🌟 **Investment Advisor Pro** - Prototype v1.0")