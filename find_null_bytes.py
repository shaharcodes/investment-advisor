#!/usr/bin/env python3
"""
Script to find exactly which file contains null bytes
"""

import os
import sys

def check_for_null_bytes(filepath):
    """Check if a file contains null bytes"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        null_positions = []
        for i, byte in enumerate(content):
            if byte == 0:
                null_positions.append(i)
        
        return null_positions
    except Exception as e:
        return f"Error: {e}"

def test_import_step_by_step():
    """Test imports step by step to isolate the problem"""
    
    print("🔍 STEP-BY-STEP IMPORT TEST")
    print("=" * 40)
    
    # Test 1: Basic imports
    try:
        print("1. Testing basic imports...")
        import pandas as pd
        import numpy as np
        print("   ✅ pandas, numpy: OK")
    except Exception as e:
        print(f"   ❌ Basic imports failed: {e}")
        return
    
    # Test 2: Streamlit
    try:
        print("2. Testing streamlit...")
        import streamlit as st
        print("   ✅ streamlit: OK")
    except Exception as e:
        print(f"   ❌ streamlit failed: {e}")
        return
    
    # Test 3: Market data
    try:
        print("3. Testing market data...")
        from src.data.market_data import MarketDataFetcher
        print("   ✅ market_data: OK")
    except Exception as e:
        print(f"   ❌ market_data failed: {e}")
        print("   🔍 Checking src/data/market_data.py for null bytes...")
        nulls = check_for_null_bytes('src/data/market_data.py')
        if nulls:
            print(f"   📍 Found null bytes at positions: {nulls[:10]}...")
        return
    
    # Test 4: Technical analysis
    try:
        print("4. Testing technical analysis...")
        from src.analyzers.technical_analysis import TechnicalAnalyzer
        print("   ✅ technical_analysis: OK")
    except Exception as e:
        print(f"   ❌ technical_analysis failed: {e}")
        print("   🔍 Checking src/analyzers/technical_analysis.py for null bytes...")
        nulls = check_for_null_bytes('src/analyzers/technical_analysis.py')
        if nulls:
            print(f"   📍 Found null bytes at positions: {nulls[:10]}...")
        return
    
    # Test 5: Recommendation engine
    try:
        print("5. Testing recommendation engine...")
        from src.models.recommendation_engine import RecommendationEngine
        print("   ✅ recommendation_engine: OK")
    except Exception as e:
        print(f"   ❌ recommendation_engine failed: {e}")
        print("   🔍 Checking src/models/recommendation_engine.py for null bytes...")
        nulls = check_for_null_bytes('src/models/recommendation_engine.py')
        if nulls:
            print(f"   📍 Found null bytes at positions: {nulls[:10]}...")
        return
    
    # Test 6: Main streamlit app
    try:
        print("6. Testing main streamlit app...")
        import src.app.streamlit_app
        print("   ✅ main streamlit app: SUCCESS!")
        print("   🎉 NO NULL BYTES ISSUE!")
    except Exception as e:
        print(f"   ❌ main streamlit app failed: {e}")
        print("   🔍 Checking src/app/streamlit_app.py for null bytes...")
        nulls = check_for_null_bytes('src/app/streamlit_app.py')
        if nulls:
            print(f"   📍 Found null bytes at positions: {nulls[:10]}...")
        else:
            print("   🤔 No null bytes found in main file, issue may be in dependencies")

if __name__ == "__main__":
    test_import_step_by_step()
