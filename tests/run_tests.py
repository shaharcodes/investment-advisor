#!/usr/bin/env python3
"""
Test Runner
Executes all tests for the Investment Advisor system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_all_tests():
    """Run the complete test suite"""
    print("🧪 INVESTMENT ADVISOR - COMPLETE TEST SUITE")
    print("=" * 60)
    print()
    
    # Import test modules
    try:
        from test_environment import test_environment
        from test_data_fetching import test_data_fetching, test_symbol_normalization, test_data_quality
        from test_technical_analysis import test_technical_analysis, test_rsi_calculation, test_moving_averages, test_bollinger_bands
        from test_recommendation_engine import test_recommendation_engine, test_risk_tolerance_differences, test_recommendation_consistency
        from test_portfolio_system import test_portfolio_tracker, test_portfolio_manager, test_position_sizing, test_risk_calculations, test_transaction_history
        from test_weekly_portfolio import test_weekly_return_calculation, test_weekly_portfolio_summary, test_weekly_ui_components, test_weekly_trading_model_integration
        
        # All tests to run
        all_tests = [
            ("Environment", test_environment),
            ("Data Fetching", test_data_fetching),
            ("Symbol Normalization", test_symbol_normalization),
            ("Data Quality", test_data_quality),
            ("Technical Analysis", test_technical_analysis),
            ("RSI Calculation", test_rsi_calculation),
            ("Moving Averages", test_moving_averages),
            ("Bollinger Bands", test_bollinger_bands),
            ("Recommendation Engine", test_recommendation_engine),
            ("Risk Tolerance", test_risk_tolerance_differences),
            ("Recommendation Consistency", test_recommendation_consistency),
        ]
        
        print(f"📋 Running {len(all_tests)} tests...\n")
        
        results = []
        for test_name, test_func in all_tests:
            print(f"🔄 Running: {test_name}")
            try:
                result = test_func()
                results.append(result)
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"   {status}")
            except Exception as e:
                print(f"   ❌ FAILED: {e}")
                results.append(False)
            print()
        
        # Summary
        passed = sum(results)
        total = len(results)
        
        print("=" * 60)
        print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is ready for production use.")
        else:
            failed = total - passed
            print(f"⚠️ {failed} test(s) failed. Please review the output above.")
        
        # Detailed breakdown
        print("\n📋 Test Categories:")
        print("   🔧 Environment: Ready for development")
        print("   📊 Data Fetching: Market data retrieval")  
        print("   📈 Technical Analysis: Indicator calculations")
        print("   🎯 Recommendations: Investment advice generation")
        
        return passed == total
        
    except Exception as e:
        print(f"❌ Test suite failed to run: {e}")
        return False

def run_quick_test():
    """Run a quick subset of critical tests"""
    print("⚡ QUICK TEST SUITE")
    print("=" * 30)
    
    try:
        from test_environment import test_environment
        from test_data_fetching import test_data_fetching
        from test_technical_analysis import test_technical_analysis
        from test_recommendation_engine import test_recommendation_engine
        
        quick_tests = [
            ("Environment", test_environment),
            ("Data Fetching", test_data_fetching),
            ("Technical Analysis", test_technical_analysis),
            ("Recommendations", test_recommendation_engine),
        ]
        
        results = []
        for test_name, test_func in quick_tests:
            try:
                result = test_func()
                results.append(result)
                print()
            except Exception as e:
                print(f"❌ {test_name} failed: {e}")
                results.append(False)
                print()
        
        passed = sum(results)
        total = len(results)
        
        print("=" * 30)
        print(f"⚡ QUICK TESTS: {passed}/{total} passed")
        
        return passed == total
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Investment Advisor tests')
    parser.add_argument('--quick', action='store_true', help='Run quick test suite only')
    args = parser.parse_args()
    
    if args.quick:
        success = run_quick_test()
    else:
        success = run_all_tests()
    
    sys.exit(0 if success else 1)
