# StockTuna Documentation

#### Sections

- [Overview](README.md)
- [\_\_init\_\_( )](./__init__.md)
- [sma( bars, period )](./sma.md)
- [sma_graph( bars, periods, symbol)](sma_graph.md)
- [~ema( bars, period )](ema.md)
- [ema_graph( bars, periods, symbol)](ema_graph.md)
- [rsi( bars, period )](rsi.md)
- [rsi_graph( bars, period, symbol)](rsi_graph.md)
#### StockTuna.ema( bars, period )

This method calculates the Exponential Moving Average (EMA), a commonly used indicator in financial trading to smooth out price data by creating a constantly updated average price over a specific period. The method takes two arguments:

- `bars` - a list of bar objects from Alpaca
- `period` - an integer to specify the number of bars to include in the average calculation.

The EMA is computed by first calculating the EMA of the initial period using a simple average of the closing prices. Then, for each subsequent price, the EMA is adjusted by adding a fraction of the difference between the current price and the previous EMA. This fraction, often called the smoothing factor, is determined by the formula: $2 / (\text{period} + 1)$. This rolling calculation efficiently updates the average without recalculating the entire average each time. The method returns a list with the EMA values, prepending None for the positions where the EMA cannot be computed due to insufficient data at the start of the series.

The method returns the list of integers. Here's an example of its use:

```commandline
from stocktuna.stocktuna import PaperTuna
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta

# config
timeframe = TimeFrame.Day
investment_time = 365
start_date = (datetime.now() - timedelta(days=investment_time)).strftime('%Y-%m-%d')

# create PaperTuna object
tuna = PaperTuna(1)

# Fetch historical data for PNC stock using the PaperTuna API
bars = tuna.stocktuna.api.get_bars("PNC", timeframe, start=start_date, limit=50)

# Calculate SMA values
ema_values = tuna.stocktuna.ema(bars, 14)

# show output for example
print("Bars: ", len(bars))
print("EMA Values: ", len(ema_values))
print(ema_values)
```

The output would then look like:

```commandline
No API credentials provided directly. Attempting to load from 'api_auth.py'...
'api_auth.py' found in directory: [REDACTED] Loading credentials from file...
API credentials successfully loaded from 'api_auth.py'.

Connecting to Alpaca API using base URL: https://paper-api.alpaca.markets
Using Alpaca Key: AKAJ... (redacted for security)
API connection complete.

Bars:  50
EMA Values:  50
[None, None, None, None, None, None, None, None, None, None, None, None, None, 153.85285714285715, 153.9404761904762, 154.10574603174604, 153.8969798941799, 153.23338257495593, 152.67159823162848, 152.1580518007447, 151.37564489397872, 151.2975589081149, 151.04855105369958, 150.89674424653964, 150.80784501366767, 150.86679901184533, 150.96455914359927, 151.29995125778603, 151.69329109008123, 151.6288522780704, 150.8036719743277, 150.44718237775066, 149.83155806071724, 149.75935031928827, 149.54743694338316, 149.3317786842654, 149.12354152636334, 149.12573598951488, 148.61030452424623, 148.51159725434673, 148.66071762043381, 148.68595527104264, 148.42116123490362, 148.17433973691647, 147.80309443866093, 147.5786818468395, 147.21485760059423, 147.046209920515, 146.865381931113, 146.90999767363127]
```