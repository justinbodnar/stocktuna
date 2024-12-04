# StockTuna v0.2.0 Pre-Alpha

Developed by Justin Bodnar  
Website: [justinbodnar.com](http://justinbodnar.com)  
Email: [contact@justinbodnar.com](mailto:contact@justinbodnar.com)

## About StockTuna

**StockTuna** is a Python library currently in pre-alpha development, designed for processing stock market and securities historical data. It integrates seamlessly with the Alpaca API to provide users with real-time and historical market data, facilitating the development of sophisticated algorithmic trading strategies. Visit the official website at [stocktuna.com](http://stocktuna.com) for more information and resources.

### Features of StockTuna

- **Alpaca API Integration**: Direct access to real-time and historical market data via Alpaca.
- **Advanced Data Analysis**: Tools for comprehensive analysis, including trend identification and predictive modeling.
- **Customizable Framework**: Easily adaptable to fit specific analytical needs or market conditions.

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
   pip install -e .
   ```
   This installs the package in editable mode, so any changes you make to the source files will be reflected immediately.

3. **Set Up API Credentials**:
   StockTuna requires an Alpaca API key and secret to access market data. You have two options:
   - **Option 1**: Directly provide credentials in your code. Example:
     ```python
     from stocktuna.stocktuna import StockTuna
     tuna = StockTuna(alpaca_key='your_alpaca_key', alpaca_secret='your_alpaca_secret', verbosity=2)
     ```
   - **Option 2**: Use a local `api_auth.py` file:
     - Rename `examples/api_auth_template.py` to `api_auth.py`.
     - Add your Alpaca API credentials to the file.

4. **Run the Example**:
   Navigate to the `examples/` directory and run `example.py` to see how to use StockTuna to fetch data and generate SMA plots:
   ```bash
   cd examples
   python3 example.py
   ```
   This script demonstrates how to use the library to pull historical stock data and visualize SMA (Simple Moving Average) for various periods.

### Prerequisites

- Python 3.7 or higher.
- An Alpaca API account (sign up at [alpaca.markets](https://alpaca.markets)).

## To Do

- **Expand Indicator Functions**: Need more mathematical functions like SMA, EMA, etc.

## About the Author

Justin Bodnar is the developer behind StockTuna. For more information about his work or to get in touch, visit [justinbodnar.com](http://justinbodnar.com) or send an email to [contact@justinbodnar.com](mailto:contact@justinbodnar.com).
