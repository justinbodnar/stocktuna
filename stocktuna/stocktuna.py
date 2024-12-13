import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
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
			print("API connection complete.\n")
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

	def sma_graph(self, bars, periods, symbol):
		"""Generate and save a graph of price data and SMAs for given periods."""
		# Extract closing prices and dates
		closes = [bar.c for bar in bars]
		dates = [bar.t for bar in bars]

		# Calculate SMAs for each period
		sma_data = {}
		for period in periods:
			sma_data[period] = self.sma(bars, period)

		# Plot the closing prices
		plt.figure(figsize=(12, 6))
		plt.plot(dates, closes, label="Price", linewidth=1.5)

		# Plot each SMA
		for period, sma_values in sma_data.items():
			plt.plot(dates, sma_values, label=f"SMA {period}", linestyle='--')

		# Assuming you have at least two periods in 'periods' list and sma_data contains valid data
		if len(periods) >= 2:
			buy_signals = []
			sell_signals = []
			for i in range(1, len(dates)):
				# Skip the loop iteration if any SMA value is None
				if sma_data[periods[0]][i] is None or sma_data[periods[1]][i] is None or \
						sma_data[periods[0]][i - 1] is None or sma_data[periods[1]][i - 1] is None:
					continue

				# Check for crossover to determine buy/sell signals
				if (sma_data[periods[0]][i] > sma_data[periods[1]][i] and
						sma_data[periods[0]][i - 1] <= sma_data[periods[1]][i - 1]):
					buy_signals.append(dates[i])
				elif (sma_data[periods[0]][i] < sma_data[periods[1]][i] and
					  sma_data[periods[0]][i - 1] >= sma_data[periods[1]][i - 1]):
					sell_signals.append(dates[i])

		# Plot buy and sell signals
		for date in buy_signals:
			plt.scatter(date, closes[dates.index(date)], color='green', marker='^', s=100)  # green triangle for buys
		for date in sell_signals:
			plt.scatter(date, closes[dates.index(date)], color='red', marker='v', s=100)  # red triangle for sells

		# Add labels, title, and legend
		plt.title(f"Price and SMAs for {symbol}", fontsize=16)
		plt.xlabel("Date", fontsize=12)
		plt.ylabel("Price", fontsize=12)
		plt.legend()
		plt.grid(True)

		# Prepare the filename
		period_str = "_".join(map(str, periods))
		filename = f"charts/sma_{period_str}_{symbol}_chart.png"

		# Create the charts directory if it doesn't exist
		os.makedirs("charts", exist_ok=True)

		# Save the chart
		plt.savefig(filename)
		plt.close()

		# Log the saved file
		if self.verbosity > 0:
			print(f"Chart saved to {filename}")

	def ema(self, bars, period):
		"""Exponential Moving Average (EMA) calculation."""
		if len(bars) < period:
			raise ValueError(f"Not enough data to calculate the {period}-period EMA. Need at least {period} bars.")
		closes = [bar.c for bar in bars]

		# Calculate the multiplier for weighting the EMA
		multiplier = 2 / (period + 1)

		# Start by using the first period's SMA as the initial EMA value
		initial_ema = sum(closes[:period]) / period
		ema_values = [initial_ema]

		# Use the formula to calculate EMA for the rest
		for i in range(period, len(closes)):
			current_ema = (closes[i] - ema_values[-1]) * multiplier + ema_values[-1]
			ema_values.append(current_ema)

		return [None] * (period - 1) + ema_values

	def ema_graph(self, bars, periods, symbol):
		"""Generate and save a graph of price data and EMAs for given periods."""
		# Extract closing prices and dates
		closes = [bar.c for bar in bars]
		dates = [bar.t for bar in bars]

		# Calculate EMAs for each period
		ema_data = {}
		for period in periods:
			ema_data[period] = self.ema(bars, period)

		# Plot the closing prices
		plt.figure(figsize=(12, 6))
		plt.plot(dates, closes, label="Price", linewidth=1.5)

		# Plot each EMA
		for period, ema_values in ema_data.items():
			plt.plot(dates, ema_values, label=f"EMA {period}", linestyle='--')

		# Assuming you have at least two periods in 'periods' list and ema_data contains valid data
		if len(periods) >= 2:
			buy_signals = []
			sell_signals = []
			for i in range(1, len(dates)):
				# Skip the loop iteration if any EMA value is None
				if ema_data[periods[0]][i] is None or ema_data[periods[1]][i] is None or \
						ema_data[periods[0]][i - 1] is None or ema_data[periods[1]][i - 1] is None:
					continue

				# Check for crossover to determine buy/sell signals
				if (ema_data[periods[0]][i] > ema_data[periods[1]][i] and
						ema_data[periods[0]][i - 1] <= ema_data[periods[1]][i - 1]):
					buy_signals.append(dates[i])
				elif (ema_data[periods[0]][i] < ema_data[periods[1]][i] and
					  ema_data[periods[0]][i - 1] >= ema_data[periods[1]][i - 1]):
					sell_signals.append(dates[i])

		# Plot buy and sell signals
		for date in buy_signals:
			plt.scatter(date, closes[dates.index(date)], color='green', marker='^', s=100)  # green triangle for buys
		for date in sell_signals:
			plt.scatter(date, closes[dates.index(date)], color='red', marker='v', s=100)  # red triangle for sells

		# Add labels, title, and legend
		plt.title(f"Price and EMAs for {symbol}", fontsize=16)
		plt.xlabel("Date", fontsize=12)
		plt.ylabel("Price", fontsize=12)
		plt.legend()
		plt.grid(True)

		# Prepare the filename
		period_str = "_".join(map(str, periods))
		filename = f"charts/ema_{period_str}_{symbol}_chart.png"

		# Create the charts directory if it doesn't exist
		os.makedirs("charts", exist_ok=True)

		# Save the chart
		plt.savefig(filename)
		plt.close()

		# Log the saved file
		if self.verbosity > 0:
			print(f"Chart saved to {filename}")

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

	def rsi_graph(self, bars, period, symbol):
		"""Generate and save a graph of RSI values and price data for a given period."""
		# Extract dates, prices, and RSI values
		dates = [bar.t for bar in bars]
		prices = [bar.c for bar in bars]
		rsi_values = self.rsi(bars, period)

		# Create the figure and axes
		fig, ax1 = plt.subplots(figsize=(12, 6))

		# Plot price data on the primary y-axis
		ax1.plot(dates, prices, label="Price", color='black', linewidth=1.5)
		ax1.set_xlabel("Date", fontsize=12)
		ax1.set_ylabel("Price", fontsize=12, color='black')
		ax1.tick_params(axis='y', labelcolor='black')

		# Plot RSI values on a secondary y-axis
		ax2 = ax1.twinx()
		ax2.plot(dates[period - 1:], rsi_values, label=f"RSI {period}", color='blue', linewidth=1.5)
		ax2.axhline(70, color='red', linestyle='--', linewidth=1, label="Overbought (70)")
		ax2.axhline(30, color='green', linestyle='--', linewidth=1, label="Oversold (30)")
		ax2.set_ylabel("RSI", fontsize=12, color='blue')
		ax2.tick_params(axis='y', labelcolor='blue')

		# Define buy and sell signals based on RSI threshold crossovers
		buy_signals = [dates[i] for i in range(period - 1, len(rsi_values) + period - 1) if
					   rsi_values[i - (period - 1)] > 30 and rsi_values[i - (period - 1) - 1] <= 30]
		sell_signals = [dates[i] for i in range(period - 1, len(rsi_values) + period - 1) if
						rsi_values[i - (period - 1)] < 70 and rsi_values[i - (period - 1) - 1] >= 70]

		# Plot buy and sell signals on the price chart
		for date in buy_signals:
			ax1.scatter(date, prices[dates.index(date)], color='green', marker='^', s=100)  # green triangle for buys
		for date in sell_signals:
			ax1.scatter(date, prices[dates.index(date)], color='red', marker='v', s=100)  # red triangle for sells

		# Add title and legends
		plt.title(f"RSI ({period}) and Price for {symbol}", fontsize=16)
		ax1.legend(loc="upper left")
		ax2.legend(loc="upper right")

		# Grid and formatting
		plt.grid(True)

		# Prepare the filename
		filename = f"charts/rsi_{period}_{symbol}_chart.png"

		# Create the charts directory if it doesn't exist
		os.makedirs("charts", exist_ok=True)

		# Save the chart
		plt.savefig(filename)
		plt.close()

		# Log the saved file
		if self.verbosity > 0:
			print(f"RSI chart with price data saved to {filename}")
