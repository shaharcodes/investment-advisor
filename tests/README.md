# 🧪 Investment Advisor Test Suite

## 🎯 Purpose

This directory contains comprehensive tests to ensure the investment advisor system components work correctly and reliably.

## 🧪 Test Files

| File | Purpose | Tests |
|------|---------|-------|
| `run_tests.py` | **Main test runner** | Executes all tests with detailed summary |
| `test_environment.py` | Environment verification | Python, packages, virtual env |
| `test_data_fetching.py` | Market data retrieval | US/Israeli data, validation, quality |
| `test_technical_analysis.py` | TA calculations | RSI, SMA, Bollinger Bands, indicators |
| `test_recommendation_engine.py` | Investment recommendations | Risk tolerance, consistency, logic |
| `demo.py` | **Live demonstration** | End-to-end system showcase |
| **ARCHIVE FOLDER** | | |
| `test_pandas_ta_compatibility.py` | pandas_ta compatibility test | Archive - compatibility issues confirmed |
| `manual_pandas_ta_test.py` | Manual pandas_ta test | Archive - not installed as expected |
| `archive_installation_test.py` | Installation attempt test | Archive - decided against due to risks |

## 🚀 How to Run Tests

### Run All Tests (Recommended)
```bash
python tests/run_tests.py
```

### Run Quick Test Suite
```bash
python tests/run_tests.py --quick
```

### Run Individual Test Files
```bash
# Environment check
python tests/test_environment.py

# Market data tests
python tests/test_data_fetching.py

# Technical analysis tests
python tests/test_technical_analysis.py

# Recommendation engine tests
python tests/test_recommendation_engine.py

# Live demo
python tests/demo.py
```

### Using pytest (if installed)
```bash
# Run all tests with pytest
pytest tests/ -v

# Run specific test file
pytest tests/test_technical_analysis.py -v
```

## ✅ What Tests Verify

### 🔧 Environment Tests
- ✅ Python version and virtual environment
- ✅ Critical packages installed (pandas, yfinance, streamlit, etc.)
- ✅ Optional packages detection

### 📊 Market Data Tests  
- ✅ US market data (AAPL, NVDA) retrieval
- ✅ Israeli market data (TEVA) with auto-conversion (.TA suffix)
- ✅ Symbol validation and error handling
- ✅ Data format consistency and quality checks

### 📈 Technical Analysis Tests
- ✅ RSI calculations (0-100 range validation)
- ✅ Moving averages (SMA 20, SMA 50)
- ✅ Bollinger Bands (upper/lower relationships)
- ✅ All indicator calculations and data integrity

### 🎯 Recommendation Engine Tests
- ✅ Buy/Sell/Hold recommendation generation
- ✅ Risk tolerance differentiation (conservative/moderate/aggressive)
- ✅ Confidence scoring and consistency
- ✅ Recommendation logic validation

## 🔧 Adding New Tests

When you add new features to the investment advisor:

1. **Create test file** for the new component
2. **Follow naming convention**: `test_[component_name].py`
3. **Add to run_tests.py** to include in test suite
4. **Test both success and failure cases**

## 📋 Test Guidelines

### ✅ Good Tests
- Test specific functionality
- Use predictable test data
- Verify expected outputs
- Handle edge cases

### ❌ Avoid
- Tests dependent on internet (for core functionality)
- Tests that modify real trading accounts
- Overly complex test scenarios

## 🎯 When to Run Tests

- ✅ **Before development** - Verify environment
- ✅ **After changes** - Ensure nothing broke
- ✅ **Before deployment** - Final verification
- ✅ **Weekly** - Regular health check

## 🚨 Critical for Financial Software

Since this is a **financial trading system**, testing is especially important:

- **Accuracy** - Ensure calculations are correct
- **Reliability** - Prevent costly errors
- **Consistency** - Verify repeatable results
- **Safety** - Catch issues before real trading

**Always run tests before making trading decisions!**