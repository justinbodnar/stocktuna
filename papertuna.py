import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta

# import api auth information
from api_auth import alpaca_key, alpaca_secret

# global settings
verbosity = 2

# function to return alpaca api connection
def get_api_connection():
	# API auth and connection settings
	BASE_URL = 'https://paper-api.alpaca.markets'
	if verbosity > 0:
		print("\nConnecting to Alpaca API")
	api = tradeapi.REST(alpaca_key, alpaca_secret, BASE_URL, api_version='v2')
	if verbosity > 0:
		print("API connection complete")
	return api

def sma(bar, period):
	# Ensure that we have enough bars to calculate the SMA
	if len(bars) < period:
		raise ValueError(f"Not enough data to calculate the {period}-period SMA. Need at least {period} bars.")
	# Extract closing prices
	closes = [bar.c for bar in bars]
	# Calculate the SMA for each point after the initial period
	sma_values = []
	for i in range(period - 1, len(closes)):
		sma = sum(closes[i - period + 1:i + 1]) / period
		sma_values.append(sma)
	return sma_values

def save_closing_prices_and_sma_plot(bars, period, symbol, filename=None):
	# Set default filename if none provided
	if filename is None:
		filename = f'charts/{symbol}_closing_prices_sma{period}_plot.png'

	# Extract closing prices and corresponding dates
	closes = [bar.c for bar in bars]
	dates = [bar.t.strftime("%m-%d-%y") if isinstance(bar.t, datetime) else bar.t for bar in bars]
	# Calculate SMA values using the provided function
	sma_values = sma(bars, period)
	# Create the plot
	plt.figure(figsize=(10, 6))
	plt.plot(dates[-len(closes):], closes, label='Closing Prices', color='blue', linestyle='-', linewidth=1)
	plt.plot(dates[-len(sma_values):], sma_values, label=f'SMA{period}', color='orange', linestyle='-', linewidth=1)
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title(f'{symbol} Closing Prices and SMA{period} Over Time')
	plt.xticks(ticks=range(0, len(dates), max(1, len(dates) // 12)), rotation=45)
	plt.grid(True)
	plt.legend()
	plt.tight_layout()
	plt.savefig(filename)
	plt.close()
	print(f"Plot saved as {filename}")

# connect to alpaca api
api = get_api_connection()

# Fetch historical data for SMA calculation
symbol = 'AAPL'
timeframe = TimeFrame.Day  # Use the TimeFrame class to specify 'Day'
n = 500
start_date = (datetime.now() - timedelta(days=n)).strftime('%Y-%m-%d')

if verbosity > 0:
	print("\nSettings for analysis")
	print("Symbol:", symbol)
	print("Timeframe:", timeframe)
	print("N:", n)

# Fetch daily price bars for the given symbol using the limit parameter only
bars = api.get_bars(symbol, timeframe, start=start_date, limit=n)

if verbosity > 0:
	print("\nPulled", len(bars), "bars from API")

sma10 = sma( bars, 10 )
if verbosity > 0:
	print("\nSMA10 entries:",len(sma10))

save_closing_prices_and_sma_plot(bars,10,symbol)
save_closing_prices_and_sma_plot(bars,20,symbol)
save_closing_prices_and_sma_plot(bars,50,symbol)
save_closing_prices_and_sma_plot(bars,100,symbol)
save_closing_prices_and_sma_plot(bars,200,symbol)
