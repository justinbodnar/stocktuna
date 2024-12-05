from stocktuna.stocktuna import PaperTuna
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta

# Instantiate the PaperTuna class with ./api_auth.py for paper trading
tuna = PaperTuna(verbosity=2)

# Set the stock symbol, timeframe, and number of days to look back
symbol = 'AAPL'
timeframe = TimeFrame.Day
start_date = (datetime.now() - timedelta(days=500)).strftime('%Y-%m-%d')

# Fetch historical data for the specified symbol using the PaperTuna API
bars = tuna.stocktuna.api.get_bars(symbol, timeframe, start=start_date, limit=500)

# Save plots for different SMA periods
tuna.stocktuna.save_closing_prices_and_sma_plot(bars, 10, symbol)
tuna.stocktuna.save_closing_prices_and_sma_plot(bars, 20, symbol)
tuna.stocktuna.save_closing_prices_and_sma_plot(bars, 50, symbol)
tuna.stocktuna.save_closing_prices_and_sma_plot(bars, 100, symbol)
tuna.stocktuna.save_closing_prices_and_sma_plot(bars, 200, symbol)
