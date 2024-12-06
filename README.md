# StockTuna v0.2.0 Pre-Alpha

Developed by Justin Bodnar  
Website: [justinbodnar.com](http://justinbodnar.com)  
Email: [contact@justinbodnar.com](mailto:contact@justinbodnar.com)

## About StockTuna

**StockTuna** is a Python library currently in pre-alpha development, designed for processing stock market and securities historical data. It integrates with the Alpaca API to provide users with real-time and historical market data, facilitating the development of sophisticated algorithmic trading strategies. Visit the official website at [stocktuna.com](http://stocktuna.com) for more information and resources.

### Features of StockTuna

- **Paper and Live Trading Modes**: Two subclasses (`PaperTuna` and `LiveTuna`) make it easy to switch between paper trading and live trading.
- **Alpaca API Integration**: Direct access to real-time and historical market data via Alpaca.
- **Indicator Functions**: Includes functions for calculating **Simple Moving Average (SMA)** and **Relative Strength Index (RSI)**.
- **Advanced Data Analysis**: Tools for comprehensive analysis, including trend identification and predictive modeling.

### Available Classes and Functions

- **PaperTuna**: Initializes a `PaperTuna` object for paper trading using Alpaca's paper trading API.
- **LiveTuna**: Initializes a `LiveTuna` object for live trading using Alpaca's live trading API.
- **StockTuna**: The core class that handles API connection and provides utility functions for data analysis.
  - **`get_api_connection(base_url)`**: Establishes a connection to the Alpaca API using provided credentials.
  - **`sma(bars, period)`**: Calculates the Simple Moving Average (SMA) over a specified period.
  - **`rsi(bars, period)`**: Calculates the Relative Strength Index (RSI) for the given period.
  - **`save_closing_prices_and_indicators_plot(bars, sma_periods, rsi_period, symbol, filename)`**: Saves a plot of closing prices, SMAs, and RSI to visualize stock trends.

### Example: Moving Average Crossover Strategy

The repository includes an example file called `moving_average_crossover_strategy.py`. This script demonstrates the use of `PaperTuna` to fetch historical stock data, calculate SMA values, and identify buy/sell signals based on a moving average crossover strategy. The script also generates and saves a chart showing the stock's closing prices along with buy/sell indicators and SMAs.

## Get Started

Follow these steps to set up and start using StockTuna:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/StockTuna.git
   cd StockTuna
   ```

2. **Install Dependencies**:
   Install the required dependencies by running:
   ```bash
   pip install .
   ```

3. **Set Up API Credentials**:
   StockTuna requires an Alpaca API key and secret to access market data. You have two options:
   - **Option 1**: Directly provide credentials in your code. Example:
     ```python
     from stocktuna.stocktuna import PaperTuna
     tuna = PaperTuna(alpaca_key='your_alpaca_key', alpaca_secret='your_alpaca_secret', verbosity=2)
     ```
   - **Option 2**: Use a local `api_auth.py` file:
     - Rename `examples/api_auth_template.py` to `api_auth.py`.
     - Add your Alpaca API credentials to the file.

4. **Run the Example**:
   Navigate to the `examples/` directory and run `moving_average_crossover_strategy.py` to see how to use StockTuna to fetch data and generate SMA plots:
   ```bash
   cd examples
   python3 moving_average_crossover_strategy.py
   ```
   This script demonstrates how to use the library to pull historical stock data, calculate moving averages, and visualize them along with buy and sell signals. The default example uses the `PaperTuna` subclass for paper trading.

### Prerequisites

- Python 3.7 or higher.
- An Alpaca API account (sign up at [alpaca.markets](https://alpaca.markets)).

## To Do

- **Expand Indicator Functions**: Need more mathematical functions like SMA, EMA, etc.

## About the Author

Justin Bodnar is the developer behind StockTuna. For more information about his work or to get in touch, visit [justinbodnar.com](http://justinbodnar.com) or send an email to [contact@justinbodnar.com](mailto:contact@justinbodnar.com).

