# Moving Average Crossover Strategy Analysis

This analysis was generated using the Python script located at `./examples/moving_average_crossover_strategy_bruteforce.py`.

The script backtested a crossover strategy using simple moving averages (SMA) for all combinations of SMA(x) and SMA(y), where \( x, y in [1, 30] \). The strategy was tested against various stock market indices defined in `./stocktuna/cannedtuna.py`.

Below are the best-performing \( x \) and \( y \) values for each stock index, along with their corresponding percentage gain:

| **Index**         | **Best SMA(x, y)** | **Gain (%)** |
|:------------------:|:------------------:|:------------:|
| NYSE Fang         |        1, 3        |    25.30%    |
| DJIA              |        3, 4        |    7.87%     |
| NASDAQ 100        |       17, 21       |    10.83%    |
| S&P 500           |        0, 0        |    0.00%     |
| Russell 2000      |        0, 0        |    0.00%     |