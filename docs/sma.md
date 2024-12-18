# StockTuna Documentation

#### Sections

- [Overview](README.md)
- [\_\_init\_\_( )](./__init__.md)
- [~sma( bars, period )](./sma.md)
- [sma_graph( bars, periods, symbol)](sma_graph.md)
- [ema( bars, period )](ema.md)
- [ema_graph( bars, periods, symbol)](ema_graph.md)
- [rsi( bars, period )](rsi.md)
- [rsi_graph( bars, period, symbol)](rsi_graph.md)

#### StockTuna.sma( bars, period )

This method calculates the Simple Moving Average (SMA), a commonly used indicator in financial trading to smooth out price data by creating a constantly updated average price over a specific period. The method takes two arguments:

- `bars` - a list of bar objects from Alpaca
- `period` - an integer to specify the number of bars to include in the average calculation.

The SMA is computed by first calculating the sum of the closing prices for the initial period, then continuously adjusting this sum by subtracting the oldest price and adding the newest one as the window moves forward with each new bar. This rolling calculation efficiently updates the average without recalculating the sum from scratch each time. The method returns a list with the SMA values, prepending None for the positions where the SMA cannot be computed due to insufficient data at the start of the series.

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
sma_values = tuna.stocktuna.sma(bars, 14)

# show output for example
print("Bars: ", len(bars))
print("SMA Values: ", len(sma_values))
print(sma_values)
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
SMA Values:  50

[None, None, None, None, None, None, None, None, None, None, None, None, None, 153.85285714285715, 154.0742857142857, 154.1157142857143, 154.32071428571427, 154.11714285714285, 153.87071428571429, 153.49357142857144, 152.8714285714286, 152.5257142857143, 152.13857142857142, 151.66785714285714, 151.56571428571425, 151.47428571428568, 151.1435714285714, 150.85499999999996, 150.8364285714285, 150.55285714285705, 150.0457142857142, 149.98928571428564, 149.7614285714285, 149.79499999999993, 149.92928571428567, 149.72499999999994, 149.60642857142852, 149.55142857142852, 149.1964285714285, 148.95499999999993, 148.81428571428566, 148.48357142857137, 147.94428571428563, 147.61285714285708, 147.60928571428562, 147.4657142857142, 147.39571428571418, 147.15714285714276, 146.97999999999988, 146.92785714285702]
```