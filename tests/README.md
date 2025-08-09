# Investment Advisor Test Suite

## 🎯 Purpose

This directory contains tests to ensure the investment advisor system components work correctly and reliably.

## 🧪 Test Files

| File | Purpose | Tests |
|------|---------|-------|
| `test_technical_analysis.py` | TA calculations | RSI, SMA, analyzer setup |
| `test_data_fetching.py` | Market data | US/Israeli data, format validation |
| `run_tests.py` | Test runner | Executes all tests with summary |

## 🚀 How to Run Tests

### Run All Tests
```bash
python tests/run_tests.py
```

### Run Individual Test Files
```bash
# Test technical analysis only
python tests/test_technical_analysis.py

# Test data fetching only  
python tests/test_data_fetching.py
```

### Using pytest (if installed)
```bash
# Run all tests with pytest
pytest tests/

# Run specific test file
pytest tests/test_technical_analysis.py -v
```

## ✅ What Tests Verify

### 📈 Technical Analysis Tests
- ✅ RSI calculations return values 0-100
- ✅ SMA calculations are reasonable
- ✅ Analyzer initializes correctly
- ✅ TA library integration works

### 📊 Data Fetching Tests  
- ✅ US market data (AAPL) accessible
- ✅ Israeli market data (TEVA) accessible
- ✅ Data format consistency (DataFrame, datetime index)
- ✅ Data quality (High >= Close >= Low)

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