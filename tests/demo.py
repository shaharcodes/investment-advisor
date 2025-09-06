#!/usr/bin/env python3
"""
Investment Advisor Demo
Quick end-to-end demonstration of the system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def demo_analysis(symbol='AAPL'):
    """Demonstrate complete analysis workflow"""
    print(f"🎯 DEMO: Analyzing {symbol}")
    print("=" * 30)
    
    try:
        # Import components
        from src.data.market_data import MarketDataFetcher
        from src.analyzers.technical_analysis import TechnicalAnalyzer
        from src.models.recommendation_engine import RecommendationEngine
        
        # Step 1: Fetch data
        print("1. Fetching market data...")
        fetcher = MarketDataFetcher()
        data = fetcher.get_stock_data(symbol, period='1mo')
        stock_info = fetcher.get_stock_info(symbol)
        
        if data.empty:
            print(f"   ❌ No data available for {symbol}")
            return False
        
        print(f"   ✅ Retrieved {len(data)} data points")
        print(f"   📊 Company: {stock_info.get('company_name', 'N/A')}")
        
        # Step 2: Technical analysis
        print("2. Performing technical analysis...")
        analyzer = TechnicalAnalyzer()
        analysis = analyzer.calculate_all_indicators(data)
        
        latest = analysis.iloc[-1]
        print(f"   📈 Current price: ${latest['close']:.2f}")
        print(f"   📊 RSI: {latest['rsi']:.1f}")
        
        # Step 3: Generate recommendation
        print("3. Generating recommendation...")
        engine = RecommendationEngine(risk_tolerance='moderate')
        recommendation = engine.generate_recommendation(analysis, stock_info)
        
        print(f"   🎯 Recommendation: {recommendation['action']}")
        print(f"   🔥 Confidence: {recommendation['confidence']}%")
        print(f"   💭 Reasoning: {recommendation['reasoning']}")
        
        print(f"\n✅ Demo completed successfully for {symbol}!")
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def run_demo():
    """Run demonstration with multiple stocks"""
    print("🚀 INVESTMENT ADVISOR - DEMO")
    print("=" * 40)
    
    test_stocks = ['AAPL', 'NVDA', 'TEVA']
    results = []
    
    for stock in test_stocks:
        try:
            result = demo_analysis(stock)
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Error with {stock}: {e}")
            results.append(False)
            print()
    
    passed = sum(results)
    total = len(results)
    
    print("=" * 40)
    print(f"📋 DEMO SUMMARY: {passed}/{total} stocks analyzed successfully")
    
    if passed > 0:
        print("🎉 Investment Advisor is working!")
    else:
        print("⚠️ System needs attention")

if __name__ == "__main__":
    run_demo()
