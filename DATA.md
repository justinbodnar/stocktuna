# DATA SOURCE

Data set can be found at https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

# DATA LEVEL 0

Raw data consists of day[0], day[1], day[2]...

Each day has an open price, and a close price

DATA = [ open[0], open[2], open[3] ... close[0], close[1], close[2] ... ]

If the final close price is higher than the initial open price, we assume it was a good investment.

TAG = [ True ]

# DATA LEVEL 1

Raw data consists of day[0], day[1], day[2]...

On each day there's a percentage change, calculated as change[n] = [ (open[n]-close[n]) * (100/close[n]) ]

DATA = [ change[0], change[1], change[2] ... ]

If the final close price is higher than the initial open price, we assume it was a good investment.

TAG = [ True ]

# DATA LEVEL 2

TBA
