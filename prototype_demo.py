#!/usr/bin/env python3
"""
Investment Advisor Prototype Demo
End-to-end demonstration of the investment recommendation system
"""

import sys
import os

# Add src to path
sys.path.append('src')

def main():
    """
    Main demo function - launches the Streamlit app
    """
    print("🚀 INVESTMENT ADVISOR PROTOTYPE DEMO")
    print("=" * 50)
    print()
    print("📊 Features included in this prototype:")
    print("  ✅ Real-time stock data fetching (AAPL, MSFT, etc.)")
    print("  ✅ Technical analysis (RSI, MACD, SMA, Bollinger Bands)")
    print("  ✅ AI-powered buy/sell/hold recommendations")
    print("  ✅ Interactive web dashboard")
    print("  ✅ Mobile-responsive design")
    print("  ✅ Risk tolerance settings")
    print("  ✅ Position sizing suggestions")
    print()
    print("🎯 To launch the web interface:")
    print("  Run: streamlit run src/app/streamlit_app.py")
    print()
    print("📱 The app will be accessible on:")
    print("  🖥️  Computer: http://localhost:8501")
    print("  📱 Mobile: http://your-ip:8501")
    print()
    print("🧪 You can also test individual components:")
    print("  📊 Data: python src/data/market_data.py")
    print("  📈 Analysis: python src/analyzers/technical_analysis.py")
    print("  🎯 Recommendations: python src/models/recommendation_engine.py")
    print()
    
    # Quick system check
    print("🔍 Quick system check...")
    
    try:
        from src.data.market_data import MarketDataFetcher
        from src.analyzers.technical_analysis import TechnicalAnalyzer
        from src.models.recommendation_engine import RecommendationEngine
        print("  ✅ All modules imported successfully")
        
        # Test basic functionality
        fetcher = MarketDataFetcher()
        analyzer = TechnicalAnalyzer()
        engine = RecommendationEngine()
        print("  ✅ All components initialized")
        
        print("\n🎉 PROTOTYPE READY TO RUN!")
        print("=" * 50)
        print()
        
        # Ask user if they want to launch
        response = input("🚀 Launch Streamlit app now? (y/n): ").strip().lower()
        
        if response in ['y', 'yes']:
            print("\n📊 Launching Investment Advisor Dashboard...")
            print("⏳ Please wait while the app starts...")
            print("🌐 Your browser should open automatically")
            print("📱 For mobile access, use your IP address instead of localhost")
            print()
            
            # Launch Streamlit
            os.system("streamlit run src/app/streamlit_app.py")
        else:
            print("\n✨ Demo ready! Launch manually with:")
            print("   streamlit run src/app/streamlit_app.py")
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        print("\n🔧 Please ensure virtual environment is activated:")
        print("   powershell -ExecutionPolicy Bypass")
        print("   venv\\Scripts\\Activate.ps1")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    main()