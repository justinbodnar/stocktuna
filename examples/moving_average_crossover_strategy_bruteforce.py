
from stocktuna.stocktuna import PaperTuna
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta

# config
verbosity = 1
tuna = PaperTuna(verbosity)
# use this for an entire index
index = tuna.stocktuna.nyse_fang
# use this for a single stock
#index = ["RCAT"]
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
	# Calculate SMA values
	sma_short_values = tuna.stocktuna.sma(bars, short_period)
	sma_long_values = tuna.stocktuna.sma(bars, long_period)

	# Ensure SMA values have the same length as dates
	sma_short_values_full = [None] * (len(bars) - len(sma_short_values)) + sma_short_values
	sma_long_values_full = [None] * (len(bars) - len(sma_long_values)) + sma_long_values

	# Identify Buy/Sell Signals using Moving Average Crossover
	buy_signals = []
	sell_signals = []

	for i in range(long_period, len(bars)):
		if sma_short_values_full[i] is not None and sma_long_values_full[i] is not None and sma_short_values_full[i - 1] is not None and sma_long_values_full[i - 1] is not None:
			if sma_short_values_full[i] > sma_long_values_full[i] and sma_short_values_full[i - 1] <= sma_long_values_full[i - 1]:
				buy_signals.append(bars[i].t.strftime('%Y-%m-%d'))
			elif sma_short_values_full[i] < sma_long_values_full[i] and sma_short_values_full[i - 1] >= sma_long_values_full[i - 1]:
				sell_signals.append(bars[i].t.strftime('%Y-%m-%d'))

	dates = [bar.t.strftime('%Y-%m-%d') for bar in bars]
	closing_prices = [bar.c for bar in bars]

	# Initialize variables for paper trading
	original_cash_balance = cash_balance = 100000  # Starting with $100,000
	position = 0  # Initial position (number of shares held)
	investment_value = 0  # Value of the current investments
	transactions = []  # List of all transactions

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
	final_stock_change = ((closing_prices[-1] - closing_prices[0]) / closing_prices[0]) * 100
	strategy_change = ((final_value - original_cash_balance) / original_cash_balance) * 100
	performance_difference = strategy_change - final_stock_change

	if verbosity > 1:
		# Print the transactions
		for date, action, price, qty, new_balance in transactions:
			if action == "BUY":
				print(f"{date}: Buy {qty} shares at ${price:.2f}, New Balance (Cash + Investment): ${new_balance:.2f}")
			elif action == "SELL":
				profit = round(qty * price - (qty * transactions[transactions.index((date, action, price, qty, new_balance)) - 1][2]), 2)
				print(f"{date}: Sell {qty} shares at ${price:.2f}, New Balance: ${new_balance:.2f}, Profit: ${profit:.2f}")

	if verbosity > 0:
		# Print overall stock and strategy performance
		print(f"Stock change over the period: {final_stock_change:.2f}%")
		print(f"Strategy change over the period: {strategy_change:.2f}%")
		print(f"Performance difference (strategy vs. holding): {performance_difference:.2f}%")

		# Print the final value with commas
		print(f"Final Portfolio Value: ${final_value:,.2f}")

	return "{:.2f}".format(performance_difference)

# Variables to track highest and lowest averages and their respective parameters
highest_avg = float('-inf')
lowest_avg = float('inf')
best_params = [ 0, 0 ]
worst_params = [ 0, 0 ]

# Calculate the total number of valid combinations
total_combinations = sum(1 for short_period in short_period_range for long_period in long_period_range if short_period < long_period)
tests_run = 0  # Counter for tests completed

# Iterate through all combinations of short_period and long_period
for short_period in short_period_range:
	for long_period in long_period_range:
		if short_period >= long_period:
			# Skip invalid combinations where short SMA is not less than long SMA
			continue
		# Update and print progress
		tests_run += 1
		progress = (tests_run / total_combinations) * 100
		print(f"\n-[ Progress: {tests_run}/{total_combinations} tests run ({progress:.2f}%) ]-")
		print(f"Highest Average: {highest_avg:.2f}% with parameters short_period={best_params[0]}, long_period={best_params[1]}")

		# List to store results for the current parameter combination
		results = []

		print("Testing SMA"+str(short_period)+" and SMA"+str(long_period))
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

# Print the results
print(f"\nHighest Average: {highest_avg:.2f}% with parameters short_period={best_params[0]}, long_period={best_params[1]}")
print(f"Lowest Average: {lowest_avg:.2f}% with parameters short_period={worst_params[0]}, long_period={worst_params[1]}")
print("Started at",starttime)
print("Ended at: ",datetime.now().strftime("%m-%d %H:%M:%S"))