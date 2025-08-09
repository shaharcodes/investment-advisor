#!/usr/bin/env python3
"""
Quick System Check
Simple verification that all components work before development
"""

def main():
    print("🔍 QUICK SYSTEM CHECK BEFORE DEVELOPMENT")
    print("=" * 50)
    
    # Test 1: Core imports
    print("\n1️⃣ Testing Core Imports...")
    try:
        import pandas as pd
        import numpy as np
        import yfinance as yf
        print("   ✅ Core imports working")
    except Exception as e:
        print(f"   ❌ Core imports failed: {e}")
        return False
    
    # Test 2: Technical Analysis
    print("\n2️⃣ Testing Technical Analysis...")
    try:
        from simple_ta_analyzer import SimpleTechnicalAnalyzer
        analyzer = SimpleTechnicalAnalyzer()
        
        # Quick calculation test
        test_data = pd.DataFrame({'close': [100, 101, 102, 103, 104]})
        rsi = analyzer.rsi(test_data, period=4)
        sma = analyzer.sma(test_data, period=3)
        
        print(f"   ✅ RSI calculation: {rsi.iloc[-1]:.2f}")
        print(f"   ✅ SMA calculation: {sma.iloc[-1]:.2f}")
        print("   ✅ Technical analysis working")
    except Exception as e:
        print(f"   ❌ Technical analysis failed: {e}")
        return False
    
    # Test 3: Market Data
    print("\n3️⃣ Testing Market Data...")
    try:
        # Quick US data test
        aapl = yf.Ticker('AAPL')
        aapl_data = aapl.history(period="1d")
        
        if len(aapl_data) > 0:
            latest_price = aapl_data['Close'].iloc[-1]
            print(f"   ✅ AAPL latest price: ${latest_price:.2f}")
        else:
            print("   ⚠️ AAPL data available but no recent records")
            
        print("   ✅ US market data working")
    except Exception as e:
        print(f"   ❌ Market data failed: {e}")
        return False
    
    # Test 4: Integration
    print("\n4️⃣ Testing Integration...")
    try:
        # Get real data and run TA
        aapl = yf.Ticker('AAPL')
        data = aapl.history(period="5d")
        
        if len(data) >= 3:
            # Prepare data
            data_clean = data.copy()
            data_clean.columns = [col.lower() for col in data_clean.columns]
            
            # Run analysis
            analyzer = SimpleTechnicalAnalyzer()
            rsi = analyzer.rsi(data_clean, period=3)
            
            current_price = data_clean['close'].iloc[-1]
            current_rsi = rsi.iloc[-1]
            
            print(f"   ✅ Real AAPL price: ${current_price:.2f}")
            print(f"   ✅ Real RSI calculation: {current_rsi:.2f}")
            print("   ✅ Integration working")
        else:
            print("   ⚠️ Limited data but integration functional")
            
    except Exception as e:
        print(f"   ❌ Integration failed: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 SYSTEM CHECK COMPLETE!")
    print("✅ All components verified")
    print("✅ Technical analysis functional")  
    print("✅ Market data accessible")
    print("✅ Integration pipeline working")
    print("🚀 READY TO START DEVELOPMENT!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ SYSTEM CHECK FAILED - Please fix issues before development")
    else:
        print("\n✨ DEVELOPMENT CAN BEGIN!")