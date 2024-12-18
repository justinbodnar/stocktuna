# StockTuna Documentation

[Previous Page: Overview](./overview.md)

#### StockTuna.\_\_init\_\_( self, alpaca_key=None, alpaca_secret=None, verbosity=1 )

You can initiate a connection to the Alpaca API either using hardcoded variables, or storing them in `./api_auth.py`

- `alpaca_key`: Optional input. Your Alpaca API key, provided as a string.
- `alpaca_secret`: Optional input. Your Alpaca secret key, also a string, used alongside the API key for secure authentication.
- `verbosity`: An integer that controls the amount of logging output. Currently the code handles `0` for no output, or `1` for verbose output. Higher values increase the detail of logs, useful for debugging.

Example `api_auth.py` file:

```commandline
alpaca_key = "blakblahblahblah"
alpaca_secret = "blahblahblahblah"
```

#### Paper Trading with `PaperTuna`
To simulate trading activities without financial risk, initialize `PaperTuna` with your Alpaca credentials:
```python
papertuna = PaperTuna(alpaca_key='your_key', alpaca_secret='your_secret')
```
This class sets the API connection to the paper trading endpoint, allowing you to test strategies in a sandbox environment.

#### Live Trading with `LiveTuna`
For real transactions, use `LiveTuna`:
```python
livetuna = LiveTuna(alpaca_key='your_key', alpaca_secret='your_secret')
```
This initializes a connection to the live trading API endpoint for actual trading operations.

[Next Page: StockTuna.sma()](./sma.md)