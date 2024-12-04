from stocktuna.stocktuna import StockTuna
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta

# Hardcoded Alpaca API credentials (replace these with your real keys)
#alpaca_key = ""
#alpaca_secret = ""

# Instantiate the StockTuna class with hardcoded auth
#tuna = StockTuna(alpaca_key, alpaca_secret, verbosity=2)

# Instantiate the StockTuna class with ./api_auth.py
tuna = StockTuna(verbosity=2)

# Set the stock symbol, timeframe, and number of days to look back
symbol = 'AAPL'
timeframe = TimeFrame.Day
start_date = (datetime.now() - timedelta(days=500)).strftime('%Y-%m-%d')

# Fetch historical data for the specified symbol
bars = tuna.api.get_bars(symbol, timeframe, start=start_date, limit=500)

# Save plots for different SMA periods
tuna.save_closing_prices_and_sma_plot(bars, 10, symbol)
tuna.save_closing_prices_and_sma_plot(bars, 20, symbol)
tuna.save_closing_prices_and_sma_plot(bars, 50, symbol)
tuna.save_closing_prices_and_sma_plot(bars, 100, symbol)
tuna.save_closing_prices_and_sma_plot(bars, 200, symbol)
