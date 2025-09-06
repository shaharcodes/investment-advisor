#!/usr/bin/env python3
"""
Investment Advisor Streamlit Dashboard
Interactive web interface for the investment recommendation system
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from src.data.market_data import MarketDataFetcher
    from src.analyzers.technical_analysis import TechnicalAnalyzer
    from src.models.recommendation_engine import RecommendationEngine
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Investment Advisor Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better mobile experience
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .recommendation-buy {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .recommendation-sell {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
    .recommendation-hold {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class InvestmentDashboard:
    """Main dashboard class for the investment advisor"""
    
    def __init__(self):
        """Initialize dashboard components"""
        self.data_fetcher = MarketDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        self.recommendation_engine = None
        
        # Initialize session state
        if 'data' not in st.session_state:
            st.session_state.data = None
        if 'analysis' not in st.session_state:
            st.session_state.analysis = None
        if 'recommendation' not in st.session_state:
            st.session_state.recommendation = None
    
    def render_sidebar(self):
        """Render the sidebar with controls"""
        st.sidebar.title("🎯 Settings")
        
        # Stock selection
        symbol = st.sidebar.text_input("Stock Symbol", value="AAPL", help="Enter stock ticker (e.g., AAPL, MSFT)")
        
        # Time period
        period = st.sidebar.selectbox(
            "Analysis Period",
            ["1mo", "3mo", "6mo", "1y", "2y"],
            index=1,
            help="Select historical data period"
        )
        
        # Risk tolerance
        risk_tolerance = st.sidebar.selectbox(
            "Risk Tolerance",
            ["conservative", "moderate", "aggressive"],
            index=1,
            help="Select your risk preference"
        )
        
        # Investment amount
        investment_amount = st.sidebar.number_input(
            "Investment Amount ($)",
            min_value=100,
            max_value=1000000,
            value=10000,
            step=500,
            help="Total amount to invest"
        )
        
        # Analysis button
        analyze_button = st.sidebar.button("🔍 Analyze Stock", type="primary")
        
        return symbol.upper(), period, risk_tolerance, investment_amount, analyze_button
    
    def fetch_and_analyze(self, symbol: str, period: str, risk_tolerance: str):
        """Fetch data and perform analysis with enhanced error handling"""
        with st.spinner(f"Fetching data for {symbol}..."):
            # Validate symbol first
            is_valid, normalized_symbol, suggestions = self.data_fetcher.validate_symbol(symbol)
            
            if not is_valid:
                st.error(f"❌ Invalid stock symbol: **{symbol}**")
                if suggestions:
                    st.info("💡 **Suggestions:**")
                    for suggestion in suggestions[:5]:
                        st.write(f"   • {suggestion}")
                else:
                    st.info("💡 **Tips:**")
                    st.write("   • Check the spelling of the stock symbol")
                    st.write("   • For Israeli stocks, try: TEVA, ICL, CHKP, NICE, BANK-HAPOALIM")
                    st.write("   • For international stocks, add market suffix (e.g., .L for London)")
                return None, None, None, None
            
            # Fetch market data
            data = self.data_fetcher.get_stock_data(symbol, period=period)
            
            if data.empty:
                st.error(f"❌ No price data available for **{normalized_symbol}**")
                st.warning("This could be due to:")
                st.write("   • Stock may be delisted or suspended")
                st.write("   • Limited trading activity")
                st.write("   • Data provider temporary issues")
                
                # Get stock info even if no price data
                stock_info = self.data_fetcher.get_stock_info(symbol)
                if 'error' not in stock_info:
                    st.info(f"ℹ️ **Company Info:** {stock_info.get('company_name', 'N/A')}")
                    if stock_info.get('suggestions'):
                        st.info("💡 **Alternative symbols to try:**")
                        for suggestion in stock_info['suggestions'][:3]:
                            st.write(f"   • {suggestion}")
                
                return None, None, None, stock_info
            
            # Get stock info
            stock_info = self.data_fetcher.get_stock_info(symbol)
            
            # Check stock info quality
            if 'error' in stock_info:
                st.warning(f"⚠️ Limited company information available for {normalized_symbol}")
                st.write(f"   Error: {stock_info['error']}")
            elif stock_info.get('data_quality'):
                quality = stock_info['data_quality']
                if quality in ['1/4', '2/4']:
                    st.warning(f"⚠️ Limited company data quality: {quality}")
            
            # Perform technical analysis
            analysis = self.analyzer.calculate_all_indicators(data)
            
            # Generate recommendation
            self.recommendation_engine = RecommendationEngine(risk_tolerance=risk_tolerance)
            recommendation = self.recommendation_engine.generate_recommendation(analysis, stock_info)
            
            st.success(f"✅ Successfully analyzed **{normalized_symbol}** with {len(data)} data points")
            
            return data, analysis, recommendation, stock_info
    
    def render_header(self, symbol: str):
        """Render the main header"""
        st.markdown(f'<h1 class="main-header">📈 Investment Advisor Pro - {symbol}</h1>', unsafe_allow_html=True)
        st.markdown("---")
    
    def render_stock_overview(self, data: pd.DataFrame, stock_info: dict):
        """Render stock overview section"""
        if data.empty:
            return
        
        latest = data.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Current Price",
                f"${latest['close']:.2f}",
                f"{latest['daily_return']*100:.2f}%" if 'daily_return' in data.columns else None
            )
        
        with col2:
            market_cap = stock_info.get('market_cap', 0)
            if market_cap > 1e9:
                market_cap_str = f"${market_cap/1e9:.1f}B"
            elif market_cap > 1e6:
                market_cap_str = f"${market_cap/1e6:.1f}M"
            else:
                market_cap_str = f"${market_cap:,.0f}"
            
            st.metric("Market Cap", market_cap_str)
        
        with col3:
            pe_ratio = stock_info.get('pe_ratio', 0)
            st.metric("P/E Ratio", f"{pe_ratio:.1f}" if pe_ratio else "N/A")
        
        with col4:
            beta = stock_info.get('beta', 0)
            st.metric("Beta", f"{beta:.2f}" if beta else "N/A")
        
        # Company info
        if stock_info.get('company_name'):
            st.info(f"**{stock_info['company_name']}** | {stock_info.get('sector', 'N/A')} | {stock_info.get('industry', 'N/A')}")
    
    def render_recommendation(self, recommendation: dict, investment_amount: float):
        """Render recommendation section"""
        if not recommendation:
            return
        
        action = recommendation['action']
        confidence = recommendation['confidence']
        
        # Recommendation card
        if action == 'BUY':
            card_class = "recommendation-buy"
            icon = "🟢"
        elif action == 'SELL':
            card_class = "recommendation-sell"
            icon = "🔴"
        else:
            card_class = "recommendation-hold"
            icon = "🟡"
        
        st.markdown(f"""
        <div class="{card_class}">
            <h3>{icon} Recommendation: {action}</h3>
            <p><strong>Confidence:</strong> {confidence}%</p>
            <p><strong>Reasoning:</strong> {recommendation['reasoning']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Position sizing
        if action in ['BUY', 'SELL']:
            position_size = recommendation.get('position_size_pct', 10)
            position_amount = investment_amount * (position_size / 100)
            shares = position_amount / recommendation['current_price']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Suggested Position", f"{position_size:.1f}%")
            with col2:
                st.metric("Investment Amount", f"${position_amount:,.0f}")
            with col3:
                st.metric("Estimated Shares", f"{shares:.0f}")
        
        # Detailed reasoning
        with st.expander("📋 Detailed Analysis"):
            if 'detailed_reasoning' in recommendation:
                for reason in recommendation['detailed_reasoning']:
                    st.write(reason)
    
    def render_price_chart(self, data: pd.DataFrame):
        """Render interactive price chart"""
        if data.empty:
            return
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Price & Moving Averages', 'RSI', 'MACD'),
            row_width=[0.6, 0.2, 0.2]
        )
        
        # Price and moving averages
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['open'] if 'open' in data.columns else data['close'],
                high=data['high'] if 'high' in data.columns else data['close'],
                low=data['low'] if 'low' in data.columns else data['close'],
                close=data['close'],
                name="Price"
            ),
            row=1, col=1
        )
        
        # Moving averages
        if 'sma_20' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['sma_20'], name="SMA 20", line=dict(color='orange')),
                row=1, col=1
            )
        
        if 'sma_50' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['sma_50'], name="SMA 50", line=dict(color='red')),
                row=1, col=1
            )
        
        # Bollinger Bands
        if all(col in data.columns for col in ['bb_upper', 'bb_lower']):
            fig.add_trace(
                go.Scatter(
                    x=data.index, y=data['bb_upper'], 
                    name="BB Upper", line=dict(color='gray', dash='dash')
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=data.index, y=data['bb_lower'], 
                    name="BB Lower", line=dict(color='gray', dash='dash'),
                    fill='tonexty', fillcolor='rgba(128,128,128,0.1)'
                ),
                row=1, col=1
            )
        
        # RSI
        if 'rsi' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['rsi'], name="RSI", line=dict(color='purple')),
                row=2, col=1
            )
            # RSI levels
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        if 'macd' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['macd'], name="MACD", line=dict(color='blue')),
                row=3, col=1
            )
            if 'signal' in data.columns:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data['signal'], name="Signal", line=dict(color='red')),
                    row=3, col=1
                )
            if 'histogram' in data.columns:
                fig.add_trace(
                    go.Bar(x=data.index, y=data['histogram'], name="Histogram", marker_color='green'),
                    row=3, col=1
                )
        
        # Update layout
        fig.update_layout(
            title="Technical Analysis Chart",
            xaxis_rangeslider_visible=False,
            height=800,
            showlegend=True
        )
        
        # Update y-axes
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1, range=[0, 100])
        fig.update_yaxes(title_text="MACD", row=3, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_metrics_table(self, data: pd.DataFrame):
        """Render technical indicators table"""
        if data.empty or len(data) < 2:
            return
        
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        metrics_data = []
        
        # RSI
        if 'rsi' in data.columns:
            rsi_change = latest['rsi'] - prev['rsi']
            metrics_data.append({
                'Indicator': 'RSI (14)',
                'Current': f"{latest['rsi']:.1f}",
                'Change': f"{rsi_change:+.1f}",
                'Signal': 'Oversold' if latest['rsi'] < 30 else 'Overbought' if latest['rsi'] > 70 else 'Neutral'
            })
        
        # MACD
        if 'macd' in data.columns:
            macd_change = latest['macd'] - prev['macd']
            signal = 'Bullish' if latest['macd'] > 0 else 'Bearish' if latest['macd'] < 0 else 'Neutral'
            metrics_data.append({
                'Indicator': 'MACD',
                'Current': f"{latest['macd']:.3f}",
                'Change': f"{macd_change:+.3f}",
                'Signal': signal
            })
        
        # Moving averages
        if 'sma_20' in data.columns:
            ma_change = latest['sma_20'] - prev['sma_20']
            signal = 'Above' if latest['close'] > latest['sma_20'] else 'Below'
            metrics_data.append({
                'Indicator': 'SMA 20',
                'Current': f"${latest['sma_20']:.2f}",
                'Change': f"{ma_change:+.2f}",
                'Signal': f"Price {signal}"
            })
        
        if metrics_data:
            df_metrics = pd.DataFrame(metrics_data)
            st.dataframe(df_metrics, use_container_width=True)
    
    def run(self):
        """Main app runner"""
        # Sidebar
        symbol, period, risk_tolerance, investment_amount, analyze_button = self.render_sidebar()
        
        # Header
        self.render_header(symbol)
        
        # Analysis trigger
        if analyze_button or st.session_state.data is None:
            result = self.fetch_and_analyze(symbol, period, risk_tolerance)
            
            # Handle different result cases
            if result and len(result) == 4:
                data, analysis, recommendation, stock_info = result
                
                # Store results in session state
                st.session_state.data = data
                st.session_state.analysis = analysis
                st.session_state.recommendation = recommendation
                st.session_state.stock_info = stock_info
                st.session_state.symbol = symbol
                st.session_state.last_error = None
            else:
                # Store error state
                st.session_state.data = None
                st.session_state.analysis = None
                st.session_state.recommendation = None
                st.session_state.stock_info = None
                st.session_state.symbol = symbol
                st.session_state.last_error = f"Failed to analyze {symbol}"
        
        # Display results or error messages
        if (hasattr(st.session_state, 'data') and 
            st.session_state.data is not None and 
            not st.session_state.data.empty):
            
            # Successfully analyzed - show full dashboard
            st.subheader("📊 Stock Overview")
            self.render_stock_overview(st.session_state.data, st.session_state.stock_info)
            
            st.subheader("🎯 Investment Recommendation")
            self.render_recommendation(st.session_state.recommendation, investment_amount)
            
            st.subheader("📈 Technical Analysis")
            self.render_price_chart(st.session_state.analysis)
            
            st.subheader("📋 Key Indicators")
            self.render_metrics_table(st.session_state.analysis)
            
            with st.expander("📄 Raw Data"):
                st.dataframe(st.session_state.analysis.tail(10))
                
        elif hasattr(st.session_state, 'last_error') and st.session_state.last_error:
            # Show error state with helpful information
            st.subheader("❌ Analysis Failed")
            
            st.markdown("""
            ### 🤔 What can you try?
            
            **Popular US Stocks:**
            - `AAPL` (Apple Inc.)
            - `MSFT` (Microsoft Corporation)
            - `GOOGL` (Alphabet Inc.)
            - `TSLA` (Tesla Inc.)
            - `NVDA` (NVIDIA Corporation)
            
            **Israeli Stocks (TA125/TA35):**
            - `TEVA` (Teva Pharmaceutical)
            - `ICL` (Israel Chemicals)
            - `CHKP` (Check Point Software)
            - `NICE` (NICE Ltd.)
            - `BANK-HAPOALIM` (Bank Hapoalim)
            
            **International Examples:**
            - `ASML.AS` (ASML Netherlands)
            - `SAP.F` (SAP Germany)
            - `NESN.SW` (Nestlé Switzerland)
            """)
            
        else:
            # Initial state - show welcome message
            st.info("👆 **Click 'Analyze Stock' to get started!**")
            st.markdown("""
            ### 🚀 Welcome to Investment Advisor Pro
            
            Enter a stock symbol in the sidebar and click "Analyze Stock" to:
            - Get real-time technical analysis
            - Receive AI-powered investment recommendations
            - View interactive price charts
            - See key financial metrics
            
            **Try popular symbols:** AAPL, MSFT, TEVA, GOOGL, TSLA
            """)

def main():
    """Main function"""
    dashboard = InvestmentDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()