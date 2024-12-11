# Exponential Moving Average Crossover Strategy Analysis

This analysis was generated using the Python script located at `./examples/exponential_moving_average_crossover_strategy_bruteforce.py`.

The script backtested a crossover strategy using exponential moving averages (EMA) for all combinations of EMA(x) and EMA(y), where \( x, y in [1, 30] \). The strategy was tested against various stock market indices defined in `./stocktuna/cannedtuna.py`.

Below are the best-performing \( x \) and \( y \) values for each stock index, along with their corresponding percentage gain:

| **Index**         | **Best SMA(x, y)** | **Gain (%)** |
|:------------------:|:------------------:|:------------:|
| NYSE Fang         |       24, 25       |    17.96%    |
| DJIA              |       24, 25       |    7.68%     |
| NASDAQ 100        |        0, 0        |    0.00%     |
| S&P 500           |        0, 0        |    0.00%     |
| Russell 2000      |        0, 0        |    0.00%     |