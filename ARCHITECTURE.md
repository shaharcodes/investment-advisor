# 🏗️ Investment Advisor System Architecture

## 📋 Fundamental Decisions

### 🤖 ML Architecture: Hybrid Self-Learning Weekly Trading System
**Decision Date**: 2025-01-26  
**Status**: ✅ Approved  
**Updated**: 2025-01-26 (User Requirements)

**System Type**: Pure weekly on-demand advisor (sleeps 6.5 days/week)
**Trading Frequency**: Once per week
**Operation Mode**: Weekly comprehensive analysis sessions only
**Markets**: NASDAQ, US Markets, Israeli TA125/TA35
**Mode**: 2-month simulation → Real trading

**Local ML Components**:
- Technical analysis (RSI, MACD, Bollinger Bands, etc.)
- Self-learning models (XGBoost, Random Forest with feedback loops)
- Portfolio optimization with position sizing
- Weekly portfolio risk assessment and protection planning
- Advanced order management (stop-limit, short selling, complex orders)
- Decision tracking and outcome analysis
- Transaction cost modeling

**External LLM Components**:
- News sentiment analysis (OpenAI/Anthropic APIs)
- Market analysis reports
- Investment reasoning explanations
- Israeli market news analysis (Hebrew/English)

**Self-Learning Features**:
- Records all recommendations and actual outcomes
- Analyzes prediction accuracy and adjusts models
- Improves decision quality over time
- Backtesting validation framework

**Rationale**: Weekly trading schedule reduces operational costs, self-learning improves accuracy over time, simulation period ensures system validation before real money.

## 🔄 Weekly Trading System Flow Architecture

```
Weekly Session → Portfolio Analysis → Risk Assessment → Protection Order Setup → Broker Execution
      ↓                 ↓                 ↓                    ↓                     ↓
Monday Morning     Technical Analysis   Weekly Risk       Stop-Loss Orders      24/7 Protection
Data Download      Market Conditions    Assessment        Trailing Stops        Automatic Execution
Portfolio Review   Sentiment Analysis   Protection Plan   Take-Profit Orders    Result Tracking

Continuous Broker Protection: Orders execute automatically without system running
```

### Key Integration Points:
- **Weekly Portfolio Analysis**: Comprehensive weekly review with full context
- **Continuous Protection**: Stop-loss, trailing stops, take-profit orders active 24/7 via broker
- **Weekly Protection Updates**: Review and adjust all protective orders during weekly session
- **Advanced Order Management**: All order types configured weekly, executed automatically
- **Weekly Risk Assessment**: Complete portfolio protection strategy planning
- **Weekly New Positions**: Full market analysis for new buy/sell opportunities
- **Market Coverage**: NASDAQ, US general market, Israeli TA125/TA35
- **Self-Learning Loop**: Decision tracking → outcome analysis → model improvement
- **Simulation Mode**: 2-month backtesting before real trading
- **Cost Optimization**: Minimal API usage, maximum efficiency with continuous protection

## 🚀 Development Sequence

### Phase 1: Core Trading System (Weeks 1-5)
**Priority**: High | **Dependencies**: None

1. **Environment Setup** (Week 1)
   - Python 3.8+ installation
   - Virtual environment creation
   - Dependency installation (71 packages)
   - API key configuration (including Israeli market data)

2. **Multi-Market Data Collection** (Week 1-2)
   - US Markets: Yahoo Finance, Alpha Vantage, Finnhub
   - Israeli Markets: Tel Aviv Stock Exchange data (TA125, TA35)
   - News sources: US financial news + Israeli business news
   - Database schema for multi-market data

3. **Technical Analysis Engine** (Week 2-3)
   - TA-Lib integration for all markets
   - Custom indicators for different market characteristics
   - Pattern recognition algorithms
   - Signal generation with market-specific calibration

4. **Self-Learning ML Framework** (Week 3-4)
   - Base models: XGBoost, Random Forest with feedback mechanisms
   - Decision tracking database schema
   - Outcome analysis pipeline
   - Model retraining automation
   - Performance metrics calculation

5. **Portfolio Optimization Engine** (Week 4)
   - Position sizing algorithms
   - Transaction cost modeling (US vs Israeli commissions)
   - Risk-adjusted allocation optimization
   - Investment amount configuration system

6. **Decision Recording & Learning Infrastructure** (Week 5)
   - Decision tracking database setup
   - Performance monitoring framework
   - Learning feedback loop infrastructure
   - Model evaluation metrics

### Phase 3.5: Initial TA Validation Period (Weeks 6-8)
**Priority**: High | **Dependencies**: Phase 1 complete

1. **3-Week Technical Analysis Simulation** (Weeks 6-8)
   - Deploy core TA system for initial validation
   - Technical indicators only (RSI, MACD, SMA, Bollinger Bands)
   - Portfolio optimization and position sizing testing
   - Basic learning framework validation
   - **Goal**: Establish TA baseline performance and catch major issues

2. **TA Performance Analysis** (End of Week 8)
   - Technical indicator accuracy assessment
   - Position sizing effectiveness evaluation
   - Risk management validation
   - System stability and error handling verification
   - **Decision Point**: Proceed to AI enhancement or fix TA issues

### Phase 2: AI Enhancement & Market Intelligence (Weeks 9-11)
**Priority**: High | **Dependencies**: Phase 1 + TA validation complete

1. **Multi-Language LLM Setup** (Week 9)
   - OpenAI/Anthropic API integration
   - Hebrew language support for Israeli market news
   - Rate limiting and cost optimization
   - Market-specific prompt engineering

2. **Advanced News Sentiment Analysis with ML Learning** (Week 9-10)
   - US financial news sentiment pipeline with learning feedback
   - Israeli business news analysis (Hebrew/English) with performance tracking
   - Cross-market sentiment correlation analysis with model improvement
   - Economic indicators impact assessment with accuracy monitoring
   - **Self-Learning Component**: Track sentiment predictions vs actual market outcomes
   - **Feedback Loop**: Retrain sentiment models based on prediction accuracy

3. **Intelligent Report Generation** (Week 10)
   - Weekly trading recommendations with reasoning
   - Risk assessment with market-specific factors
   - Performance analysis with learning insights
   - Decision explanation generation

4. **Configuration Management Interface** (Week 11)
   - Dynamic investment amount adjustment
   - Trading frequency modification
   - Risk tolerance calibration
   - Market preference settings

### Phase 3: Full System Integration & Testing (Weeks 12-14)
**Priority**: High | **Dependencies**: Phase 2 complete

1. **Complete System Integration** (Week 12)
   - Integrate all TA and sentiment learning components
   - Unified recommendation engine with multi-factor learning
   - Cross-validation between technical and sentiment predictions
   - Performance optimization and error handling

2. **Comprehensive Testing & Validation** (Week 13)
   - End-to-end system testing
   - Data validation and quality checks
   - Learning algorithm validation
   - Performance benchmarking

3. **Production Readiness** (Week 14)
   - Final system optimization
   - Backup and recovery systems
   - User interface polishing
   - Documentation completion

### Phase 4: 2-Month Complete System Simulation (Weeks 15-22)
**Priority**: Critical | **Dependencies**: Phase 3 complete

1. **Full System Simulation Launch** (Week 15)
   - Deploy complete system with TA + ML sentiment analysis
   - Real-time data feeds for both US and Israeli markets
   - All learning algorithms operational (TA + sentiment)
   - Performance tracking for integrated system

2. **Intensive Learning Period** (Weeks 16-19)
   - **Technical Analysis Refinement**: Build on 3-week TA baseline
   - **Sentiment Analysis Learning**: News impact vs price movement correlation
   - **Cross-Factor Learning**: How TA + sentiment combine for better predictions
   - **Market Regime Detection**: Bull/bear market adaptation algorithms
   - **User Decision Learning**: Track user modifications to AI recommendations

3. **Mid-Simulation Optimization** (Weeks 20-21)
   - Compare TA-only vs TA+sentiment performance
   - Model performance evaluation and tuning
   - Learning algorithm refinement
   - Strategy adaptation based on simulation results

4. **Final System Validation** (Weeks 22)
   - Comprehensive performance analysis
   - Learning effectiveness evaluation
   - Model readiness assessment for live trading
   - Final system refinements and go/no-go decision

### Phase 5: Live Trading Deployment (Week 23+)
**Priority**: Critical | **Dependencies**: Successful 2-month simulation

1. **Live Trading Launch**
   - Transition from simulation to live trading
   - Continued learning with real money decisions
   - Performance monitoring and optimization
   - Ongoing model improvements
   - Cross-market learning (US patterns → Israeli market)

3. **User Experience Optimization** (Week 11)
   - Streamlined weekly workflow
   - Mobile-responsive dashboard
   - UI-based Notification Center with categorized display
   - Historical decision review interface

4. **Testing & Validation** (Week 12)
   - Comprehensive simulation testing
   - Model accuracy validation
   - Transaction cost verification
   - User acceptance testing

## 💻 Hardware Assessment

**Current Specs**: Intel i7-8700, 16GB RAM, GTX 1050 Ti, 461GB storage  
**Assessment**: ✅ Well-suited for hybrid approach

**Capabilities**:
- ✅ Excellent: Technical analysis, traditional ML, data processing
- ✅ Good: Small neural networks, real-time processing
- ⚠️ Limited: Large deep learning models, transformer architectures
- ❌ Cannot: Local large language models (GPT-3.5+ size)

**Expected Performance**:
- 80-90% of core functionality runs locally
- Fast response times for technical analysis
- Cost-effective NLP via external APIs ($50-200/month)

## 🎯 Success Metrics

### Phase 1 Goals:
- [x] Technical indicators working for US + Israeli markets
- [x] Portfolio tracking system with comprehensive database schema
- [x] Position sizing with risk tolerance and commission accounting  
- [x] Testing/simulation environment with virtual money
- [x] Decision tracking and recommendation accuracy measurement
- [ ] Self-learning framework operational (Phase 2)
- [ ] 2-month simulation environment validation (Phase 3.5)

### Phase 2 Goals:
- [ ] Multi-language news sentiment analysis
- [ ] Cross-market correlation insights
- [ ] Weekly recommendation reports with reasoning
- [ ] Dynamic configuration system operational
- [ ] API costs under $150/month (weekly vs daily usage)

### Phase 3 Goals:
- [ ] Simulation period shows >65% recommendation accuracy
- [ ] Self-learning demonstrates improving performance
- [ ] Transaction cost modeling within 0.1% accuracy
- [ ] System ready for real trading after 2-month simulation
- [ ] User can modify parameters during operation

## 🎯 Specific User Requirements & Implementation

### 📅 Trading Schedule & Operation Mode
- **Frequency**: Once per week (not continuous operation)
- **Runtime**: On-demand before trading sessions
- **Markets**: NASDAQ, US general market, Israeli TA125/TA35
- **Personal Use**: Single-user system initially
- **Interface**: Streamlit web-based GUI (local hosting)

### 💰 Advanced Investment Management Features
- **Real-time Portfolio Monitoring**: Continuous tracking of positions, valuations, and P&L
- **Position Sizing**: Optimal buy/sell amounts based on defined investment budget
- **Complex Order Management**: Stop-limit, stop-loss, take-profit, short selling
- **Risk-based Alerts**: Automated notifications for position deterioration or opportunities
- **Transaction Costs**: All order types, margin interest, short borrowing costs included
- **Dynamic Configuration**: Investment amount, risk parameters, and order types adjustable
- **Portfolio Protection**: AI-driven recommendations for protecting existing positions
- **Margin Management**: Buying power calculations and margin requirement monitoring

### 🧠 Comprehensive Self-Learning System
**Dual Learning Architecture**: Both Technical Analysis AND Sentiment Analysis improve over time

#### Technical Analysis Learning:
- **Indicator Accuracy Tracking**: Monitor RSI, MACD, Bollinger Bands prediction success
- **Pattern Recognition**: Learn which chart patterns actually lead to predicted movements
- **Market Condition Adaptation**: Adjust TA weights based on bull/bear market performance
- **Cross-Market Learning**: Apply US market patterns to Israeli market analysis

#### Sentiment Analysis Learning:
- **News Impact Correlation**: Track how news sentiment actually affects stock prices
- **Source Reliability**: Learn which news sources provide most predictive sentiment
- **Timing Analysis**: Understand sentiment-to-price-movement delay patterns
- **Language-Specific Learning**: Hebrew vs English news impact differences

#### Integrated Learning System:
- **Decision Tracking**: All AI recommendations AND final user decisions recorded
- **Multi-Factor Performance**: Track how TA + sentiment combinations perform
- **User Preference Learning**: Adapt to your personal trading style and risk preferences
- **Simulation Period**: 2-month comprehensive testing before real trading
- **Manual Approval**: No automatic execution - all trades require user confirmation

### 🌐 Multi-Market Data Sources
**US Markets**:
- Yahoo Finance (NASDAQ, NYSE, general US markets)
- Alpha Vantage (detailed fundamentals)
- Finnhub (real-time and news)

**Israeli Markets**:
- Tel Aviv Stock Exchange API (TA125, TA35 indices)
- Israeli financial news sources (Hebrew/English)
- Currency conversion (ILS/USD)

## 🔧 Technology Stack

**Local Processing**:
- Python 3.8+, pandas, numpy, TA-Lib
- XGBoost, scikit-learn (with feedback loops)
- Portfolio optimization (scipy.optimize)
- SQLAlchemy (decision tracking), Streamlit

**External Services**:
- OpenAI/Anthropic APIs (multi-language support)
- US Market APIs: Yahoo Finance, Alpha Vantage, Finnhub
- Israeli Market APIs: Tel Aviv Stock Exchange, Israeli financial news
- Currency APIs for ILS/USD conversion

**Infrastructure**:
- Local development on Windows 10
- SQLite database for decision tracking
- Streamlit web GUI (runs locally on http://localhost:8501)
- Weekly scheduled execution or on-demand triggers

## 🖥️ Graphical User Interface (GUI) Design

### 🌐 **Technology**: Streamlit Web Interface
**Rationale**: Perfect for data-heavy applications, easy to build/maintain, responsive design, excellent for personal use

### 📱 **Interface Components**

#### 1. **Main Dashboard**
- **Trading Mode Toggle**: Simulation vs Real Trading
- **Quick Stats**: Portfolio value, weekly P&L, success rate
- **Market Status**: US and Israeli market hours
- **Next Trading Session**: Countdown and preparation status

#### 2. **Configuration Panel** ⚙️
- **Investment Settings**: Total amount, position sizing rules
- **Risk Management**: Risk tolerance, maximum position size
- **Market Preferences**: US vs Israeli allocation ratio
- **Trading Frequency**: Weekly schedule configuration
- **Alert Settings**: Notification preferences

#### 3. **Advanced Portfolio Management** 📊
- **Real-time Positions**: Live tracking of all holdings with current valuations
- **US Holdings**: NASDAQ positions, current P&L, sector allocation, margin usage
- **Israeli Holdings**: TA125/TA35 positions, ILS/USD impact, currency hedging
- **Cash & Margin**: Available cash, buying power, margin requirements
- **Active Orders**: Pending stop-limits, shorts, complex orders
- **Risk Metrics**: Portfolio beta, concentration risk, drawdown, VaR
- **Performance Tracking**: Real-time P&L, daily/weekly returns, benchmarking

#### 4. **Comprehensive Trading Recommendations** 🎯
- **New Position Signals**: Buy/sell recommendations for new positions
- **Portfolio Protection**: Stop-loss, stop-limit, take-profit recommendations
- **Advanced Strategies**: Short selling opportunities, hedge positions
- **Risk Management**: Position sizing adjustments, diversification suggestions
- **Market Analysis**: Technical indicators, sentiment summary, volatility assessment
- **AI Insights**: LLM-generated market commentary and complex strategy reasoning
- **Order Management**: Complex order setups with precise parameters
- **Approval Interface**: Review and modify all recommendations before execution
- **Manual Confirmation**: Explicit user approval required for all trades and orders

#### 5. **Performance Tracking** 📈
- **Simulation Results**: 2-month testing performance, accuracy metrics
- **Real Trading Results**: Live performance since going live
- **Learning Progress**: Model improvement over time
- **Benchmarking**: Performance vs market indices (S&P 500, TA125)

#### 6. **Decision History** 📋
- **Past Recommendations**: Chronological list of all decisions
- **Outcome Analysis**: Success/failure rates, profit/loss tracking
- **Learning Impact**: How each decision influenced model training
- **Export Options**: CSV download for external analysis

### 📱 **Mobile Responsiveness**
- **Responsive Design**: Works on tablets and smartphones
- **Touch-Friendly**: Large buttons for configuration changes
- **Quick Access**: Essential info visible on mobile screens

## ✅ **Manual Approval Workflow**

### 🔍 **Weekly Review Process**
1. **AI Analysis**: System generates comprehensive market analysis and recommendations
2. **Recommendation Display**: Clear presentation of buy/sell signals with reasoning
3. **User Review**: Detailed examination of each recommendation
4. **Modification Options**: Ability to adjust position sizes, reject trades, or add custom orders
5. **Final Approval**: Explicit confirmation required before any execution
6. **Execution Tracking**: Both AI recommendations and final decisions recorded

### 📋 **Advanced Approval Interface Features**
- **Multi-Order Type Display**: New positions, complex orders, portfolio adjustments
- **Side-by-Side Comparison**: AI recommendation vs your modifications
- **Risk Assessment**: Impact analysis of proposed changes including margin requirements
- **Reasoning Display**: Full explanation for each AI recommendation and complex strategy
- **Override Options**: Complete control over final trading decisions and order parameters
- **Complex Order Setup**: Configure stop prices, limit prices, time-in-force, conditions
- **Portfolio Impact Analysis**: How each order affects overall portfolio risk and allocation
- **Confirmation Checklist**: Safety checks including margin requirements and risk limits
- **Export Approved List**: Download final trading plan for broker execution

### 🧠 **Learning from Approvals**
- **Pattern Recognition**: AI learns from your modification patterns
- **Preference Learning**: System adapts to your risk tolerance and preferences
- **Outcome Tracking**: Compares AI suggestions vs approved decisions vs actual results
- **Model Adaptation**: Improves future recommendations based on approval history

### 🔐 **Security & Privacy**
- **Local Hosting**: Runs on localhost:8501 (no external access)
- **Session Management**: Secure user sessions
- **Data Encryption**: Sensitive API keys encrypted at rest
- **No Auto-Trading**: Zero risk of unauthorized trade execution

### 🎨 **User Experience Features**
- **Dark/Light Themes**: Multiple visual themes
- **Interactive Charts**: Plotly-based visualizations
- **Real-time Updates**: Live data refresh during trading sessions
- **Export Capabilities**: PDF reports, CSV data export
- **Approval Workflow**: Clear review and confirmation process
- **Modification Tools**: Easy adjustment of AI recommendations

## 🔧 **Advanced Order Types & Portfolio Management**

### 📊 **Portfolio Tracking System (IMPLEMENTED)**

#### **Core Portfolio Tracker** (`src/models/portfolio_tracker.py`)
- **Manual Position Entry**: User manually inputs actual holdings from real brokerage accounts
- **Transaction Recording**: User enters completed real-world transactions for tracking
- **Live Market Valuation**: Real-time price updates for portfolio value calculation
- **TA Integration**: Uses existing TechnicalAnalyzer for buy/sell/hold suggestions on owned stocks
- **Performance History**: Tracks portfolio value changes based on market movements
- **SQLite Database**: Persistent storage for manually entered positions and transactions

#### **Portfolio Manager** (`src/models/portfolio_manager.py`)
- **Manual Entry Mode**: User manually inputs portfolio positions and transactions from real trading
- **Position Sizing Suggestions**: Calculated recommendations based on risk tolerance (user decides)
- **Market Integration**: Real-time price fetching for portfolio valuation and analysis
- **Performance Analytics**: Tracks performance based on manually entered real positions
- **Risk Assessment**: Monitors concentration and diversification of actual holdings

#### **Portfolio UI Components** (`src/app/portfolio_ui.py`)
- **Dashboard Overview**: Portfolio value, cash balance, P&L, daily returns
- **Position Tables**: Holdings with color-coded gains/losses and allocation percentages
- **Performance Charts**: Portfolio value over time with daily return visualizations
- **Testing Reports**: Comprehensive accuracy assessment for system validation
- **Risk Metrics**: Concentration analysis and diversification indicators

#### **Key Features for Manual Portfolio Management**
- **Real Portfolio Tracking**: Manual entry of actual positions from real brokerage accounts
- **Live Market Valuation**: Real-time portfolio value updates based on current market prices
- **TA Analysis for Holdings**: Uses existing TechnicalAnalyzer to generate recommendations for owned stocks
- **Performance Monitoring**: Track actual investment performance and portfolio changes
- **Manual Transaction Logging**: User enters completed trades for accurate record keeping

### 🎯 **Complex Order Types Supported**
1. **Stop-Loss Orders**: Protect existing positions from downside risk
2. **Stop-Limit Orders**: Controlled exit points with price protection
3. **Take-Profit Orders**: Automated profit-taking at target levels
4. **Trailing Stops**: Dynamic stop-loss orders that follow price movements
5. **Short Selling**: Profit from declining stocks with margin requirements
6. **Bracket Orders**: Combined stop-loss and take-profit for new positions
7. **Conditional Orders**: Orders triggered by technical indicators or news events

### 🤖 **AI-Driven Order Recommendations**
- **Portfolio Protection**: Analyze existing positions for stop-loss opportunities
- **Profit-Taking Strategies**: Identify optimal exit points for profitable positions
- **Risk Reduction**: Suggest position size reductions for over-concentrated holdings
- **Short Opportunities**: Identify overvalued stocks suitable for short selling
- **Hedge Recommendations**: Suggest protective positions against portfolio risk
- **Rebalancing Suggestions**: Maintain target allocation percentages

### 📱 **Notification Center (UI-Based System)**

#### **Design Approach**
- **UI-Based Notification Center**: All notifications displayed within the Streamlit interface (no push notifications)
- **Categorized Display**: Three distinct notification categories for organized information
- **Data-Only Recovery**: Missed notifications reconstructed from market data and news archives
- **Session Persistence**: Notifications stored and displayed when app is reopened

#### **Notification Categories**
1. **Critical Notifications** 🚨
   - Stop-loss triggers (informational - orders execute automatically)
   - Major position deterioration (>10% single-day drop)
   - Margin call warnings
   - Broker-side order execution confirmations

2. **Weekly Notifications** 📅
   - Weekly analysis ready reminders
   - Portfolio performance summaries
   - Market trend alerts affecting holdings
   - Recommended portfolio rebalancing

3. **Confirmation Notifications** ✅
   - Transaction confirmations
   - Order placement confirmations
   - Settings change confirmations
   - System status updates

#### **Data-Only Recovery System**
- **Market Data Analysis**: Reconstruct missed price movements and volatility events
- **News Archive Scanning**: Identify significant news affecting portfolio holdings
- **Portfolio Tracking**: Detect position changes and performance impacts
- **Recovery Process**: 2-3 minutes processing, 10-15% CPU usage, 2-3GB RAM temporarily
- **Accuracy**: 95%+ notification recovery rate for weekly trading needs

### 📱 **Enhanced GUI Components for Complex Orders**

#### **Order Setup Interface**
```
┌─ STOP-LOSS ORDER SETUP ─────────────────────────┐
│ Position: AAPL (100 shares @ $195.50 avg)       │
│ Current Price: $198.75 (+1.66%)                 │
│                                                  │
│ Stop Price: $185.00 [____] (5.3% below avg)     │
│ Order Type: ○ Market ● Limit                     │
│ Limit Price: $184.50 [____]                     │
│ Time in Force: ○ Day ● GTC ○ IOC                │
│                                                  │
│ Potential Loss: -$1,050 (5.4% of position)      │
│ Portfolio Impact: -0.8% overall                 │
│                                                  │
│ AI Reasoning: Technical support at $185 level,   │
│ RSI oversold bounce likely at this price.        │
│                                                  │
│ [✅ Set Stop-Loss] [❌ Cancel] [📊 Backtest]    │
└──────────────────────────────────────────────────┘
```

#### **Portfolio Risk Dashboard**
```
┌─ PORTFOLIO RISK OVERVIEW ────────────────────────┐
│ Total Value: $125,340 (+2.1% today)             │
│ Cash: $8,420 | Margin Used: $0 | Buying Power: $16,840 │
│                                                   │
│ Risk Metrics:                                     │
│ • Portfolio Beta: 1.15 (15% more volatile than market) │
│ • Max Drawdown: -4.2% (last 30 days)            │
│ • Concentration Risk: 18% in tech sector ⚠️      │
│                                                   │
│ Active Risk Management:                           │
│ • 3 Stop-loss orders active                      │
│ • 2 Take-profit orders pending                   │
│ • 1 Short position (NFLX: -$2,100)              │
│                                                   │
│ AI Recommendations: 2 new protective orders      │
│ [📊 View Details] [⚙️ Adjust Risk] [📈 Analysis] │
└───────────────────────────────────────────────────┘
```

## 📚 Documentation Standards

- Architecture decisions recorded in this document
- Code documentation using docstrings
- API documentation with examples
- User guide for dashboard operations
- Complex order setup tutorials
- Risk management procedures
- GUI component documentation
- Portfolio monitoring guides
- Deployment and maintenance procedures

---
*Last Updated: 2025-01-26*  
*Next Review: End of Phase 1* 