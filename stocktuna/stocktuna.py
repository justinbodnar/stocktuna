import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from datetime import datetime
import importlib.util
from . import cannedtuna
import os

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

		# get cannedtuna.py data
		for name, value in vars(cannedtuna).items():
			if isinstance(value, list):
				setattr(self, name, value)

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

		# Initialize gains and losses
		total_gain = 0
		total_loss = 0

		# Calculate initial average gain and loss for the first `period` bars
		for i in range(1, period):
			change = closes[i] - closes[i - 1]
			if change > 0:
				total_gain += change
			else:
				total_loss += abs(change)

		avg_gain = total_gain / (period - 1)
		avg_loss = total_loss / (period - 1) if total_loss > 0 else 1e-10  # To prevent division by zero

		# Initialize RSI values list
		rsi_values = []

		# Calculate RSI for the first `period`
		rs = avg_gain / avg_loss
		rsi_values.append(100 - (100 / (1 + rs)))

		# Calculate RSI for subsequent bars
		for i in range(period, len(closes)):
			change = closes[i] - closes[i - 1]
			gain = max(change, 0)
			loss = abs(min(change, 0))

			# Update average gain and loss using the smoothed moving average formula
			avg_gain = ((avg_gain * (period - 1)) + gain) / period
			avg_loss = ((avg_loss * (period - 1)) + loss) / period

			rs = avg_gain / avg_loss if avg_loss != 0 else 0
			rsi_value = 100 - (100 / (1 + rs))
			rsi_values.append(rsi_value)

		return rsi_values
