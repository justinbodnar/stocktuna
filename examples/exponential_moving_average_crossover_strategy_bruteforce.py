from stocktuna.stocktuna import PaperTuna
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

# config
verbosity = 1
tuna = PaperTuna(verbosity)
index = tuna.stocktuna.nasdaq_100
short_period_range = range(1, 30)
long_period_range = range(1, 30)
timeframe = TimeFrame.Day
investment_time = 365
start_date = (datetime.now() - timedelta(days=investment_time)).strftime('%Y-%m-%d')
starttime = datetime.now().strftime("%m-%d %H:%M:%S")
"""
function to backtest current strategy

takes a stock symbol, and backtests the past year worth of price data
returns the percentage difference after the tested year
"""
def backtest(symbol):
	# Fetch historical data for the specified symbol using the PaperTuna API
	bars = tuna.stocktuna.api.get_bars(symbol, timeframe, start=start_date, limit=500)
	# Calculate EMA values
	ema_short_values = tuna.stocktuna.ema(bars, short_period)
	ema_long_values = tuna.stocktuna.ema(bars, long_period)

	# Ensure EMA values have the same length as dates
	ema_short_values_full = [None] * (len(bars) - len(ema_short_values)) + ema_short_values
	ema_long_values_full = [None] * (len(bars) - len(ema_long_values)) + ema_long_values

	# Identify Buy/Sell Signals using Moving Average Crossover
	buy_signals = []
	sell_signals = []

	for i in range(long_period, len(bars)):
		# Ensure values are not None before comparison
		if ema_short_values_full[i] is not None and ema_long_values_full[i] is not None and ema_short_values_full[i - 1] is not None and ema_long_values_full[i - 1] is not None:
			# Moving Average Crossover Strategy for Buy/Sell Signals
			if ema_short_values_full[i] > ema_long_values_full[i] and ema_short_values_full[i - 1] <= ema_long_values_full[i - 1]:
				# Buy when short EMA crosses above long EMA
				buy_signals.append(bars[i].t.strftime('%Y-%m-%d'))
			elif ema_short_values_full[i] < ema_long_values_full[i] and ema_short_values_full[i - 1] >= ema_long_values_full[i - 1]:
				# Sell when short EMA crosses below long EMA
				sell_signals.append(bars[i].t.strftime('%Y-%m-%d'))

	dates = [bar.t.strftime('%Y-%m-%d') for bar in bars]
	closing_prices = [bar.c for bar in bars]

	# Initialize variables for paper trading
	original_cash_balance = cash_balance = 100000  # Starting with $100,000
	position = 0  # Initial position (number of shares held)
	initial_cash_balance = cash_balance
	investment_value = 0  # Value of the current investments

	# Iterate through the bars to simulate paper trading
	def price_at_date(bars, date):
		for bar in bars:
			if bar.t.strftime('%Y-%m-%d') == date:
				return bar.c
		return None

	def find_bar_index(bars, date):
		for idx, bar in enumerate(bars):
			if bar.t.strftime('%Y-%m-%d') == date:
				return idx
		return -1

	# List of all transactions
	transactions = []

	date_idx = 0
	for date in dates:
		if date in buy_signals:
			price = closing_prices[date_idx]
			shares_to_buy = cash_balance // price
			if shares_to_buy > 0:
				cash_balance -= shares_to_buy * price
				position += shares_to_buy
				investment_value = position * price
				transactions.append((date, 'BUY', price, shares_to_buy, cash_balance + investment_value))
		elif date in sell_signals and position > 0:
			price = closing_prices[date_idx]
			cash_balance += position * price
			investment_value = 0
			transactions.append((date, 'SELL', price, position, cash_balance))
			position = 0
		date_idx += 1

	final_value = cash_balance + (position * closing_prices[-1])

	if verbosity > 1:
		# Print the transactions
		for date, action, price, qty, new_balance in transactions:
			if action == "BUY":
				print(f"{date}: Buy {qty} shares at ${price:.2f}, New Balance (Cash + Investment): ${new_balance:.2f}")
			elif action == "SELL":
				profit = round(qty * price - (qty * transactions[transactions.index((date, action, price, qty, new_balance)) - 1][2]), 2)
				print(f"{date}: Sell {qty} shares at ${price:.2f}, New Balance: ${new_balance:.2f}, Profit: ${profit:.2f}")

		# Print the final value
		print(f"\nFinal Portfolio Value: ${final_value:.2f}")
	return "{:.2f}".format((((final_value - original_cash_balance) / original_cash_balance) * 100))

# Variables to track highest and lowest averages and their respective parameters
highest_avg = float('-inf')
lowest_avg = float('inf')
best_params = None
worst_params = None

# Calculate the total number of valid combinations
total_combinations = sum(1 for short_period in short_period_range for long_period in long_period_range if short_period < long_period)
tests_run = 0  # Counter for tests completed

# Iterate through all combinations of short_period and long_period
for short_period in short_period_range:
	for long_period in long_period_range:
		if short_period >= long_period:
			# Skip invalid combinations where short EMA is not less than long EMA
			continue

		# List to store results for the current parameter combination
		results = []

		print("Testing EMA"+str(short_period)+" and EMA"+str(long_period))
		for symbol in index:
			# Run backtest for the current symbol and parameters
			try:
				result = float(backtest(symbol))  # Convert result to a float
				results.append(result)
			except Exception as e:
				print(f"Error processing symbol {symbol} with short_period={short_period} and long_period={long_period}: {e}")

		# Calculate the average for this combination
		if results:
			avg_result = sum(results) / len(results)

			# Update highest and lowest averages
			if avg_result > highest_avg:
				highest_avg = avg_result
				best_params = (short_period, long_period)

			if avg_result < lowest_avg:
				lowest_avg = avg_result
				worst_params = (short_period, long_period)

		# Update and print progress
		tests_run += 1
		progress = (tests_run / total_combinations) * 100
		print(f"Progress: {tests_run}/{total_combinations} tests run ({progress:.2f}%)")
		print(f"\nHighest Average: {highest_avg:.2f}% with parameters short_period={best_params[0]}, long_period={best_params[1]}")

# Print the results
print(f"\nHighest Average: {highest_avg:.2f}% with parameters short_period={best_params[0]}, long_period={best_params[1]}")
print(f"Lowest Average: {lowest_avg:.2f}% with parameters short_period={worst_params[0]}, long_period={worst_params[1]}")
print("Started at",starttime)
print("Ended at: ",datetime.now().strftime("%m-%d %H:%M:%S"))
