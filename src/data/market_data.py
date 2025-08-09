import yfinance as yf
import pandas as pd
import logging

class MarketDataFetcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_stock_data(self, symbol, period="1mo"):
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                return pd.DataFrame()
            
            data.columns = [col.lower().replace(' ', '_') for col in data.columns]
            data['symbol'] = symbol
            data['daily_return'] = data['close'].pct_change()
            
            return data
        except Exception as e:
            self.logger.error(f"Error fetching {symbol}: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self, symbol):
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'beta': info.get('beta', 0),
                'current_price': info.get('currentPrice', 0)
            }
        except Exception as e:
            return {'symbol': symbol, 'error': str(e)}

if __name__ == "__main__":
    fetcher = MarketDataFetcher()
    data = fetcher.get_stock_data('AAPL')
    print(f"AAPL data: {len(data)} records")
    if not data.empty:
        print(f"Latest price: ${data['close'].iloc[-1]:.2f}")