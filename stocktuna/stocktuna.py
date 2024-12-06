import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from datetime import datetime
import os
import importlib.util

class PaperTuna:
	def __init__(self, alpaca_key=None, alpaca_secret=None, verbosity=1):
		"""Initialize the PaperTuna object for paper trading."""
		self.stocktuna = StockTuna(alpaca_key, alpaca_secret, verbosity)
		self.stocktuna.api = self.stocktuna.get_api_connection(base_url='https://paper-api.alpaca.markets')

class LiveTuna:
	def __init__(self, alpaca_key=None, alpaca_secret=None, verbosity=1):
		"""Initialize the LiveTuna object for live trading."""
		self.stocktuna = StockTuna(alpaca_key, alpaca_secret, verbosity)
		self.stocktuna.api = self.stocktuna.get_api_connection(base_url='https://api.alpaca.markets')

class StockTuna:
	def __init__(self, alpaca_key=None, alpaca_secret=None, verbosity=1):
		"""Initialize the StockTuna object with Alpaca credentials and verbosity level."""
		self.alpaca_key = alpaca_key
		self.alpaca_secret = alpaca_secret

		# Verbosity level logging
		if verbosity > 0:
			if alpaca_key and alpaca_secret:
				print("API credentials provided directly via constructor.")
			else:
				print("No API credentials provided directly. Attempting to load from 'api_auth.py'...")

		# If no API key/secret provided, attempt to load them from api_auth.py in the script's directory
		if self.alpaca_key is None or self.alpaca_secret is None:
			current_directory = os.getcwd()  # Get the current working directory
			api_auth_path = os.path.join(current_directory, "api_auth.py")

			if os.path.exists(api_auth_path):
				if verbosity > 0:
					print(f"'api_auth.py' found in directory: {current_directory}. Loading credentials from file...")
				spec = importlib.util.spec_from_file_location("api_auth", api_auth_path)
				api_auth = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(api_auth)
				self.alpaca_key = getattr(api_auth, 'alpaca_key', None)
				self.alpaca_secret = getattr(api_auth, 'alpaca_secret', None)

				if verbosity > 0:
					if self.alpaca_key and self.alpaca_secret:
						print("API credentials successfully loaded from 'api_auth.py'.")
					else:
						print("Failed to find valid credentials in 'api_auth.py'.")

		# Raise an error if API credentials are still None
		if not self.alpaca_key or not self.alpaca_secret:
			raise ValueError("Alpaca API key and secret must be provided either through the constructor or in 'api_auth.py' located in the current script's directory.")

		self.verbosity = verbosity

	def get_api_connection(self, base_url='https://paper-api.alpaca.markets'):
		"""Return Alpaca API connection."""
		if self.verbosity > 0:
			print(f"\nConnecting to Alpaca API using base URL: {base_url}")
			print(f"Using Alpaca Key: {self.alpaca_key[:4]}... (redacted for security)")

		api = tradeapi.REST(self.alpaca_key, self.alpaca_secret, base_url, api_version='v2')

		if self.verbosity > 0:
			print("API connection complete.")
		return api

	def sma(self, bars, period):
		"""Simple Moving Average (SMA) calculation."""
		if len(bars) < period:
			raise ValueError(f"Not enough data to calculate the {period}-period SMA. Need at least {period} bars.")
		closes = [bar.c for bar in bars]

		# Efficient rolling sum to calculate SMA
		sma_values = []
		rolling_sum = sum(closes[:period])
		sma_values.append(rolling_sum / period)

		for i in range(period, len(closes)):
			rolling_sum = rolling_sum - closes[i - period] + closes[i]
			sma_values.append(rolling_sum / period)

		return [None] * (period - 1) + sma_values

	def rsi(self, bars, period=14):
		"""Relative Strength Index (RSI) calculation."""
		if len(bars) < period:
			raise ValueError(f"Not enough data to calculate the {period}-period RSI. Need at least {period} bars.")
		closes = [bar.c for bar in bars]

		gains = []
		losses = []

		# Calculate initial average gain and loss
		for i in range(1, period + 1):
			change = closes[i] - closes[i - 1]
			if change > 0:
				gains.append(change)
			else:
				losses.append(abs(change))

		avg_gain = sum(gains) / period
		avg_loss = sum(losses) / period if losses else 1  # To prevent division by zero

		# Initialize RSI values list
		rsi_values = []

		# Calculate RSI for the first 'period'
		rs = avg_gain / avg_loss if avg_loss != 0 else 0
		rsi_values.append(100 - (100 / (1 + rs)))

		# Calculate RSI for subsequent bars
		for i in range(period + 1, len(closes)):
			change = closes[i] - closes[i - 1]
			gain = max(change, 0)
			loss = abs(min(change, 0))

			avg_gain = ((avg_gain * (period - 1)) + gain) / period
			avg_loss = ((avg_loss * (period - 1)) + loss) / period

			rs = avg_gain / avg_loss if avg_loss != 0 else 0
			rsi_value = 100 - (100 / (1 + rs))
			rsi_values.append(rsi_value)

		return rsi_values

	def save_closing_prices_and_indicators_plot(self, bars, sma_periods, rsi_period, symbol, filename='chart.png'):
		"""Save plot of closing prices, SMA, and RSI."""
		closes = [bar.c for bar in bars]
		dates = [bar.t.strftime("%Y-%m-%d") for bar in bars]

		# Calculate SMAs and RSI
		sma_values = {period: self.sma(bars, period) for period in sma_periods}
		rsi_values = self.rsi(bars, rsi_period)

		# Create the plot
		plt.figure(figsize=(14, 8))

		# Plot closing prices
		plt.plot(dates, closes, label='Closing Prices', color='blue')

		# Plot SMAs
		for period, values in sma_values.items():
			plt.plot(dates[len(dates) - len(values):], values, label=f'SMA {period}', linestyle='--')

		# Plot RSI in a separate subplot
		plt.plot(dates[len(dates) - len(rsi_values):], rsi_values, label=f'RSI {rsi_period}', color='green')

		plt.xlabel('Date')
		plt.ylabel('Price / Indicator Value')
		plt.title(f'{symbol} Closing Prices with Indicators')
		plt.xticks(rotation=45)
		plt.legend()
		plt.tight_layout()
		plt.savefig(filename)
		plt.close()

		if self.verbosity > 0:
			print(f"Plot saved as {filename}")
