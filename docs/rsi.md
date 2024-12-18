# StockTuna Documentation

#### Sections

- [Overview](README.md)
- [\_\_init\_\_( )](./__init__.md)
- [sma( bars, period )](./sma.md)
- [sma_graph( bars, periods, symbol)](sma_graph.md)
- [ema( bars, period )](ema.md)
- [ema_graph( bars, periods, symbol)](ema_graph.md)
- [~rsi( bars, period )](rsi.md)
- [rsi_graph( bars, period, symbol)](rsi_graph.md)

#### StockTuna.rsi( bars, period )

This method calculates the Relative Strength Index (RSI), a momentum indicator in financial trading used to gauge the velocity and magnitude of price movements. The RSI helps identify overbought or oversold conditions by measuring the ratio of upward and downward movements in a given period. The method takes two arguments:

- `bars` - a list of bar objects from Alpaca
- `period` - an integer to specify the number of bars to include in the average calculation.

The RSI is computed by first calculating the RSI of the initial period using a simple average of the gains and losses. Then, for each subsequent price, the RSI is adjusted by applying a smoothing technique. The smoothing is done by updating the average gains and average losses using the formulas:

- Average Gain = `[Previous Average Gain * (period - 1) + Current Gain] / period`
- Average Loss = `[Previous Average Loss * (period - 1) + Current Loss] / period`

This rolling calculation efficiently updates the indicator without recalculating the entire average each time. Once the average gains and losses are updated, the Relative Strength (RS) is calculated as:

$\text{RS} = \frac{\text{Average Gain}}{\text{Average Loss}}$

Finally, the RSI is derived from the RS using the formula:

$\text{RSI} = 100 - \left( \frac{100}{1 + \text{RS}} \right)$

The method returns a list with the RSI values, prepending `None` for the positions where the RSI cannot be computed due to insufficient data at the start of the series.

Here's an example of its use:

```commandline
from stocktuna.stocktuna import PaperTuna
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta

# config
timeframe = TimeFrame.Day
investment_time = 365
start_date = (datetime.now() - timedelta(days=investment_time)).strftime('%Y-%m-%d')

# create PaperTuna object
tuna = PaperTuna(0)

# Fetch historical data for PNC stock using the PaperTuna API
bars = tuna.stocktuna.api.get_bars("PNC", timeframe, start=start_date, limit=50)

# Calculate RSI values
rsi_values = tuna.stocktuna.rsi(bars, 14)

# show output for example
print("Bars: ", len(bars))
print("RSI Values: ", len(rsi_values))
print(rsi_values)
```

The output would then look like:

```commandline
No API credentials provided directly. Attempting to load from 'api_auth.py'...
'api_auth.py' found in directory: C:\Users\justi\PycharmProjects\stocktuna\examples. Loading credentials from file...
API credentials successfully loaded from 'api_auth.py'.

Connecting to Alpaca API using base URL: https://paper-api.alpaca.markets
Using Alpaca Key: AKAJ... (redacted for security)
API connection complete.

Bars:  50
RSI Values:  50
[None, None, None, None, None, None, None, None, None, None, None, None, None, 61.22748989342154, 55.12905360688284, 56.17541766109785, 51.117190110257255, 45.11801713072622, 45.308965810656716, 44.97195540014881, 40.83425524742221, 49.69907468798935, 47.388177403373795, 48.30185776151095, 48.938503599205966, 51.009455948106165, 51.73285959505654, 55.53123582855934, 57.02299964674999, 49.905019380753984, 39.760239559886465, 45.3389930925517, 41.77655895859186, 48.35114773163515, 46.519944605731574, 46.1168865410741, 45.83179213877132, 48.75312705095692, 41.86659783864863, 47.263028132108744, 50.59361491603253, 49.1132431392555, 45.18833109693696, 44.954397245992794, 42.789072785299865, 44.567915500283306, 42.11458193224128, 44.94161813632587, 44.389781475319836, 48.355943689430084]
```