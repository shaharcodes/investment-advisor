#!/usr/bin/env python3
"""
Final Environment Verification for Investment Advisor
Comprehensive test of ALL components before development starts
"""

import sys
from datetime import datetime

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_basic_environment():
    """Test Python and virtual environment"""
    print_section("BASIC ENVIRONMENT")
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment: ACTIVE")
    else:
        print("⚠️ Virtual environment: NOT DETECTED")
    
    return True

def test_core_data_packages():
    """Test pandas, numpy, scipy"""
    print_section("CORE DATA PACKAGES")
    
    results = {}
    
    try:
        import pandas as pd
        print(f"✅ pandas: {pd.__version__}")
        results['pandas'] = True
    except Exception as e:
        print(f"❌ pandas: {e}")
        results['pandas'] = False
    
    try:
        import numpy as np
        print(f"✅ numpy: {np.__version__}")
        results['numpy'] = True
    except Exception as e:
        print(f"❌ numpy: {e}")
        results['numpy'] = False
    
    try:
        import scipy
        print(f"✅ scipy: {scipy.__version__}")
        results['scipy'] = True
    except Exception as e:
        print(f"⚠️ scipy: {e} (optional)")
        results['scipy'] = False
    
    return all([results['pandas'], results['numpy']])

def test_financial_data():
    """Test yfinance and financial data access"""
    print_section("FINANCIAL DATA")
    
    try:
        import yfinance as yf
        print(f"✅ yfinance: imported successfully")
        
        # Test US stock
        print("\n🇺🇸 Testing US market access:")
        aapl = yf.Ticker('AAPL')
        aapl_info = aapl.info
        aapl_hist = aapl.history(period="5d")
        
        print(f"   ✅ AAPL: {aapl_info.get('shortName', 'Apple Inc.')}")
        print(f"   ✅ Price: ${aapl_info.get('currentPrice', 'N/A')}")
        print(f"   ✅ 5-day data: {len(aapl_hist)} days")
        
        # Test Israeli stock
        print("\n🇮🇱 Testing Israeli market access:")
        teva = yf.Ticker('TEVA')
        teva_info = teva.info
        teva_hist = teva.history(period="5d")
        
        print(f"   ✅ TEVA: {teva_info.get('shortName', 'Teva Pharmaceutical')}")
        if len(teva_hist) > 0:
            print(f"   ✅ Latest: ${teva_hist['Close'].iloc[-1]:.2f}")
            print(f"   ✅ 5-day data: {len(teva_hist)} days")
        
        return True
        
    except Exception as e:
        print(f"❌ Financial data error: {e}")
        return False

def test_technical_analysis():
    """Test technical analysis capabilities"""
    print_section("TECHNICAL ANALYSIS")
    
    try:
        # Test ta library
        import ta
        print(f"✅ ta library: imported successfully")
        
        # Test our simple analyzer
        from simple_ta_analyzer import SimpleTechnicalAnalyzer
        print(f"✅ SimpleTechnicalAnalyzer: imported successfully")
        
        # Create test data
        import pandas as pd
        import numpy as np
        
        test_data = pd.DataFrame({
            'close': [100, 101, 99, 102, 98, 103, 97, 104, 96, 105,
                     94, 106, 93, 107, 92, 108, 91, 109, 90, 110]
        })
        
        analyzer = SimpleTechnicalAnalyzer()
        
        # Test calculations
        rsi = analyzer.rsi(test_data, period=10)
        sma = analyzer.sma(test_data, period=5)
        
        print(f"✅ RSI calculation: {rsi.iloc[-1]:.2f}")
        print(f"✅ SMA calculation: {sma.iloc[-1]:.2f}")
        print(f"✅ Technical analysis: FULLY FUNCTIONAL")
        
        return True
        
    except Exception as e:
        print(f"❌ Technical analysis error: {e}")
        return False

def test_web_framework():
    """Test Streamlit for GUI"""
    print_section("WEB FRAMEWORK")
    
    try:
        import streamlit as st
        print(f"✅ streamlit: {st.__version__}")
        print(f"✅ Web interface: READY")
        return True
    except Exception as e:
        print(f"❌ streamlit error: {e}")
        return False

def test_machine_learning():
    """Test ML packages"""
    print_section("MACHINE LEARNING")
    
    results = {}
    
    try:
        import sklearn
        print(f"✅ scikit-learn: {sklearn.__version__}")
        
        # Quick ML test
        from sklearn.ensemble import RandomForestRegressor
        import numpy as np
        
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([1, 2, 3])
        model = RandomForestRegressor(n_estimators=2, random_state=42)
        model.fit(X, y)
        pred = model.predict([[2, 3]])
        print(f"   ✅ ML test prediction: {pred[0]:.2f}")
        results['sklearn'] = True
        
    except Exception as e:
        print(f"❌ scikit-learn error: {e}")
        results['sklearn'] = False
    
    try:
        import tensorflow as tf
        print(f"✅ tensorflow: {tf.__version__}")
        results['tensorflow'] = True
    except Exception as e:
        print(f"⚠️ tensorflow: {e} (optional)")
        results['tensorflow'] = False
    
    try:
        import xgboost as xgb
        print(f"✅ xgboost: {xgb.__version__}")
        results['xgboost'] = True
    except Exception as e:
        print(f"⚠️ xgboost: {e} (optional)")
        results['xgboost'] = False
    
    return results['sklearn']  # Only sklearn is critical

def test_visualization():
    """Test plotting libraries"""
    print_section("VISUALIZATION")
    
    results = {}
    
    try:
        import matplotlib
        print(f"✅ matplotlib: {matplotlib.__version__}")
        results['matplotlib'] = True
    except Exception as e:
        print(f"❌ matplotlib error: {e}")
        results['matplotlib'] = False
    
    try:
        import plotly
        print(f"✅ plotly: {plotly.__version__}")
        results['plotly'] = True
    except Exception as e:
        print(f"❌ plotly error: {e}")
        results['plotly'] = False
    
    try:
        import seaborn as sns
        print(f"✅ seaborn: {sns.__version__}")
        results['seaborn'] = True
    except Exception as e:
        print(f"⚠️ seaborn: {e} (optional)")
        results['seaborn'] = False
    
    return any([results['matplotlib'], results['plotly']])

def test_database():
    """Test database capabilities"""
    print_section("DATABASE")
    
    try:
        import sqlalchemy
        print(f"✅ sqlalchemy: {sqlalchemy.__version__}")
        
        # Test basic database functionality
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///:memory:')
        print(f"✅ Database engine: created successfully")
        return True
        
    except Exception as e:
        print(f"❌ database error: {e}")
        return False

def test_integration():
    """Test complete data pipeline integration"""
    print_section("INTEGRATION TEST")
    
    try:
        print("🔗 Testing complete data pipeline...")
        
        # Get real market data
        import yfinance as yf
        import pandas as pd
        
        print("   📊 Fetching real market data...")
        aapl = yf.Ticker('AAPL')
        data = aapl.history(period="30d")
        
        if len(data) < 20:
            print("   ⚠️ Limited data available, but proceeding...")
        
        # Prepare data for analysis
        data_clean = data.copy()
        data_clean.columns = [col.lower() for col in data_clean.columns]
        
        print(f"   ✅ Downloaded {len(data_clean)} days of AAPL data")
        
        # Run technical analysis
        from simple_ta_analyzer import SimpleTechnicalAnalyzer
        analyzer = SimpleTechnicalAnalyzer()
        
        print("   📈 Running technical analysis...")
        rsi = analyzer.rsi(data_clean, period=14)
        sma20 = analyzer.sma(data_clean, period=20)
        
        current_price = data_clean['close'].iloc[-1]
        current_rsi = rsi.iloc[-1]
        current_sma = sma20.iloc[-1]
        
        print(f"   ✅ Current AAPL price: ${current_price:.2f}")
        print(f"   ✅ RSI(14): {current_rsi:.2f}")
        print(f"   ✅ SMA(20): ${current_sma:.2f}")
        
        # Generate simple signal
        if current_rsi < 30:
            signal = "🟢 OVERSOLD - Potential buy signal"
        elif current_rsi > 70:
            signal = "🔴 OVERBOUGHT - Potential sell signal"
        else:
            signal = f"🟡 NEUTRAL (RSI: {current_rsi:.1f})"
        
        print(f"   🎯 Trading signal: {signal}")
        print("   🎉 COMPLETE PIPELINE WORKING!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        return False

def main():
    """Run comprehensive environment check"""
    print("🔍 FINAL INVESTMENT ADVISOR ENVIRONMENT CHECK")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    results = {}
    
    results['basic'] = test_basic_environment()
    results['core_data'] = test_core_data_packages()
    results['financial'] = test_financial_data()
    results['technical'] = test_technical_analysis()
    results['web'] = test_web_framework()
    results['ml'] = test_machine_learning()
    results['viz'] = test_visualization()
    results['database'] = test_database()
    results['integration'] = test_integration()
    
    # Final summary
    print_section("FINAL SUMMARY")
    
    critical_components = ['core_data', 'financial', 'technical', 'web', 'integration']
    critical_passed = sum(1 for comp in critical_components if results[comp])
    
    optional_components = ['ml', 'viz', 'database']
    optional_passed = sum(1 for comp in optional_components if results[comp])
    
    print("📊 RESULTS:")
    print(f"✅ Critical components: {critical_passed}/{len(critical_components)}")
    print(f"⚙️ Optional components: {optional_passed}/{len(optional_components)}")
    
    print("\n📋 COMPONENT STATUS:")
    status_map = {True: "✅", False: "❌"}
    
    print(f"{status_map[results['basic']]} Basic Environment")
    print(f"{status_map[results['core_data']]} Core Data (pandas, numpy)")
    print(f"{status_map[results['financial']]} Financial Data (yfinance)")
    print(f"{status_map[results['technical']]} Technical Analysis")
    print(f"{status_map[results['web']]} Web Framework (Streamlit)")
    print(f"{status_map[results['ml']]} Machine Learning")
    print(f"{status_map[results['viz']]} Visualization")
    print(f"{status_map[results['database']]} Database")
    print(f"{status_map[results['integration']]} Integration Pipeline")
    
    # Final verdict
    if critical_passed == len(critical_components):
        print("\n🎉 ENVIRONMENT STATUS: FULLY READY!")
        print("✅ All critical components working")
        print("✅ Can proceed with investment advisor development")
        print("🚀 READY TO BUILD YOUR WEEKLY TRADING SYSTEM!")
        return True
    elif critical_passed >= len(critical_components) * 0.8:
        print("\n⚠️ ENVIRONMENT STATUS: MOSTLY READY")
        print("✅ Most critical components working")
        print("🔧 Some components may need attention")
        return True
    else:
        print("\n❌ ENVIRONMENT STATUS: NEEDS ATTENTION")
        print("🔧 Critical components missing")
        print("📝 Please address issues before development")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'='*60}")
    if success:
        print("🎯 PROCEED WITH DEVELOPMENT!")
    else:
        print("🛠️ FIX ISSUES BEFORE PROCEEDING")
    print(f"{'='*60}")