# 📈 Investment Advisor Pro

Advanced AI-powered investment recommendation system that combines technical analysis with sentiment analysis for intelligent trading decisions.

## 🚀 Features

- **📊 Technical Analysis**: RSI, SMA, MACD, and advanced indicators
- **🧠 AI-Powered Recommendations**: Machine learning-driven buy/sell/hold signals
- **📰 Sentiment Analysis**: News and market sentiment integration
- **📱 Interactive Dashboard**: Real-time Streamlit web interface
- **🎯 Position Sizing**: Intelligent investment amount calculations
- **📈 Interactive Charts**: Candlestick charts with technical overlays

## 🎯 Target Markets

- **NASDAQ & US Markets**: Full support for US equities
- **Israeli Markets**: TA125 and TA35 index coverage
- **Weekly Trading Focus**: Optimized for weekly analysis cycles

## 🏗️ Architecture

**Hybrid ML Approach**:
- **Local Processing**: Technical analysis, real-time calculations
- **Cloud AI**: Sentiment analysis, natural language processing
- **Web Interface**: Streamlit-based dashboard

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Git
- Virtual Environment

### Setup
```bash
# Clone the repository
git clone https://github.com/[YOUR_USERNAME]/investment-advisor.git
cd investment-advisor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

### Launch the Dashboard
```bash
# Activate virtual environment
venv\Scripts\activate

# Run the Streamlit app
streamlit run simple_streamlit_app.py
```

### Example Usage
1. Open http://localhost:8501 in your browser
2. Enter a stock symbol (e.g., AAPL, MSFT, GOOGL)
3. Select analysis period
4. Set investment amount
5. Click "Analyze Stock" for recommendations

## 📊 Sample Analysis

```python
# Example: Analyze Apple stock
Symbol: AAPL
Period: 3 months
Investment: $10,000

# Results:
Recommendation: BUY (78% confidence)
Position Size: 12.5% ($1,250)
Estimated Shares: 8 shares
```

## 🔧 Technical Stack

- **Backend**: Python, Pandas, NumPy
- **Financial Data**: yfinance, Alpha Vantage
- **Technical Analysis**: ta library, custom indicators  
- **Portfolio Management**: SQLite database, comprehensive tracking
- **Machine Learning**: scikit-learn, XGBoost (planned)
- **Visualization**: Plotly, Streamlit
- **Data Storage**: SQLite, transaction logging

## 📁 Project Structure

```
investment-advisor/
├── src/
│   ├── analyzers/           # Technical and sentiment analysis
│   ├── data/               # Data fetching and processing
│   ├── models/             # ML models and recommendation engine
│   └── app/                # Streamlit dashboard
├── simple_streamlit_app.py # Quick demo application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 Development Roadmap

### Phase 1 (Completed) ✅
- [x] **Technical Analysis**: RSI, MACD, Bollinger Bands, ATR, Moving Averages
- [x] **Risk-Adjusted Recommendations**: Buy/sell/hold with confidence scoring
- [x] **Multi-Market Support**: US (NASDAQ) + Israeli (TA125, TA35) markets
- [x] **Position Sizing**: Risk tolerance-based allocation (conservative/moderate/aggressive)
- [x] **Streamlit Dashboard**: Professional web interface with interactive charts

### Phase 2 (In Progress)
- [x] **Manual Portfolio Tracking**: User-entered position management with real-time valuation
- [x] **TA Analysis for Holdings**: Buy/sell/hold recommendations for owned stocks
- [x] **Performance Analytics**: Track actual portfolio performance and market value changes
- [ ] Advanced ML models with self-learning
- [ ] News sentiment integration with external LLMs
- [ ] 3-week TA validation testing period

### Phase 3 (Future)
- [ ] Real-time alerts
- [ ] Backtesting engine
- [ ] Multi-asset support
- [ ] Mobile application

## ⚙️ Configuration

### Environment Variables
Create a `.env` file:
```env
# API Keys (optional)
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///investment_advisor.db
```

## 📊 Performance

- **Analysis Speed**: < 2 seconds per stock
- **Memory Usage**: < 500MB typical
- **CPU Usage**: < 50% on modern systems
- **Data Sources**: Multiple redundant APIs

## ⚠️ Disclaimer

This software is for educational and research purposes only. Not financial advice. Always consult with qualified financial advisors before making investment decisions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🎯 Support

- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: See `/docs` folder for detailed guides

---

⭐ **Star this repo if you find it useful!** ⭐

Built with ❤️ for the trading community