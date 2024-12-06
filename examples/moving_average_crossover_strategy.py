from stocktuna.stocktuna import PaperTuna
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

# Instantiate the PaperTuna class with api_auth.py for paper trading
tuna = PaperTuna(verbosity=2)

# Get the stock ticker symbol
symbol = "GME"

# Set the timeframe for the historical data and start date
timeframe = TimeFrame.Day
start_date = (datetime.now() - timedelta(days=500)).strftime('%Y-%m-%d')

# Fetch historical data for the specified symbol using the PaperTuna API
bars = tuna.stocktuna.api.get_bars(symbol, timeframe, start=start_date, limit=500)

# Set parameters for indicators
short_period = 5  # Short-term SMA for faster trend detection
long_period = 10  # Long-term SMA for slower trend detection

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

# Print Buy/Sell Signals
print("Buy Signals:")
for buy_signal in buy_signals:
	print(buy_signal)

print("\nSell Signals:")
for sell_signal in sell_signals:
	print(sell_signal)

# Plotting Buy/Sell Signals along with Closing Prices and SMAs
dates = [bar.t.strftime('%Y-%m-%d') for bar in bars]
closing_prices = [bar.c for bar in bars]

# Create the figure and axis for the plot
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot closing prices
ax1.plot(dates, closing_prices, label='Closing Prices', color='blue', linewidth=1.5)

# Plot SMA indicators
sma_short_values_full_trimmed = sma_short_values_full[-len(dates):]
sma_long_values_full_trimmed = sma_long_values_full[-len(dates):]
ax1.plot(dates, sma_short_values_full_trimmed, label=f'SMA {short_period}', color='orange', linestyle='--', linewidth=1)
ax1.plot(dates, sma_long_values_full_trimmed, label=f'SMA {long_period}', color='purple', linestyle='--', linewidth=1)

# Plot Buy/Sell signals
buy_indices = [dates.index(buy) for buy in buy_signals]
sell_indices = [dates.index(sell) for sell in sell_signals]
ax1.scatter([dates[i] for i in buy_indices], [closing_prices[i] for i in buy_indices], color='green', marker='^', s=150, label='Buy Signal', zorder=5)
ax1.scatter([dates[i] for i in sell_indices], [closing_prices[i] for i in sell_indices], color='red', marker='v', s=150, label='Sell Signal', zorder=5)

# Configure x-axis to display dates properly
ax1.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=20))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%-m-%-d'))
plt.xticks(rotation=45)

# Set labels and title
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.2f}'))
ax1.set_title(f'{symbol} Closing Prices with Buy/Sell Signals and Indicators')
ax1.legend()
plt.tight_layout()

# Save the plot as a PNG file
plt.savefig('charts/chart.png')
plt.close()

print("Chart saved as 'charts/chart.png'")

