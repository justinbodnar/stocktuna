
from stocktuna.stocktuna import PaperTuna
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

# config
verbosity = 1
tuna = PaperTuna(verbosity)
timeframe = TimeFrame.Day
investment_time = 365
start_date = (datetime.now() - timedelta(days=investment_time)).strftime('%Y-%m-%d')
short_period = 5
long_period = 10
symbol = "AA"

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
		# Ensure values are not None before comparison
		if sma_short_values_full[i] is not None and sma_long_values_full[i] is not None and sma_short_values_full[i - 1] is not None and sma_long_values_full[i - 1] is not None:
			# Moving Average Crossover Strategy for Buy/Sell Signals
			if sma_short_values_full[i] > sma_long_values_full[i] and sma_short_values_full[i - 1] <= sma_long_values_full[i - 1]:
				# Buy when short SMA crosses above long SMA
				buy_signals.append(bars[i].t.strftime('%Y-%m-%d'))
			elif sma_short_values_full[i] < sma_long_values_full[i] and sma_short_values_full[i - 1] >= sma_long_values_full[i - 1]:
				# Sell when short SMA crosses below long SMA
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

# run the backtest
final_value = backtest(symbol)
print("\nBacktesting $100,00 with the following settings:")
print("Timeframe:",timeframe)
print("Investment Time:",investment_time)
print("Start Date:",start_date)
print("Short SMA:",short_period)
print("Long SMA:",long_period)
print("Stock Ticker:",symbol)
print("\nBalance Change: "+str(final_value)+"%")
