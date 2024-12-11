# Exponential Moving Average Crossover Strategy Analysis

This analysis was generated using the Python script located at `./examples/exponential_moving_average_crossover_strategy_bruteforce.py`.

The script backtested a crossover strategy using exponential moving averages (EMA) for all combinations of EMA(x) and EMA(y), where \( x, y in [1, 30] \). The strategy was tested against various stock market indices defined in `./stocktuna/cannedtuna.py`.

Below are the best-performing \( x \) and \( y \) values for each stock index, along with their corresponding percentage gain:

| **Index**         | **Best EMA(x, y)** | **Gain (%)** |
|:------------------:|:------------------:|:------------:|
| NYSE Fang         |       2, 16        |    21.25%    |
| DJIA              |       23, 25       |    8.05%     |
| NASDAQ 100        |        1, 2        |    5.62%     |
| S&P 500           |        1, 2        |    8.17%     |
| Russell 2000      |        0, 0        |    0.00%     |