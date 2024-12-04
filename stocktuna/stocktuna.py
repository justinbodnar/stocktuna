import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from datetime import datetime
import os
import importlib.util

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
		self.api = self.get_api_connection()

	def get_api_connection(self):
		"""Return Alpaca API connection."""
		BASE_URL = 'https://paper-api.alpaca.markets'
		if self.verbosity > 0:
			print(f"\nConnecting to Alpaca API using base URL: {BASE_URL}")
			print(f"Using Alpaca Key: {self.alpaca_key[:4]}... (redacted for security)")

		api = tradeapi.REST(self.alpaca_key, self.alpaca_secret, BASE_URL, api_version='v2')
		
		if self.verbosity > 0:
			print("API connection complete.")
		return api

	def sma(self, bars, period):
		"""Simple Moving Average (SMA) calculation."""
		if len(bars) < period:
			raise ValueError(f"Not enough data to calculate the {period}-period SMA. Need at least {period} bars.")
		closes = [bar.c for bar in bars]
		sma_values = [sum(closes[i - period + 1:i + 1]) / period for i in range(period - 1, len(closes))]
		return sma_values

	def save_closing_prices_and_sma_plot(self, bars, period, symbol, filename=None):
		"""Save plot of closing prices and SMA."""
		if filename is None:
			filename = f'charts/{symbol}_closing_prices_sma{period}_plot.png'
		closes = [bar.c for bar in bars]
		dates = [bar.t.strftime("%Y-%m-%d") for bar in bars]
		sma_values = self.sma(bars, period)
		plt.figure(figsize=(10, 6))
		plt.plot(dates, closes, label='Closing Prices', color='blue')
		plt.plot(dates[len(dates) - len(sma_values):], sma_values, label=f'SMA{period}', color='orange')
		plt.xlabel('Date')
		plt.ylabel('Price')
		plt.title(f'{symbol} Closing Prices and SMA{period} Over Time')
		plt.xticks(rotation=45)
		plt.legend()
		plt.tight_layout()
		plt.savefig(filename)
		plt.close()
		if self.verbosity > 0:
			print(f"Plot saved as {filename}")
