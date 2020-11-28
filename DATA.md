# DATA SOURCE

Data set can be found at https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

# BASIC DATA ARCHITECTURE

Raw data consists of day[0], day[1], day[2], ..., day[inf]

Each day contains information about that day of the stock. ie. open price, close price, volume, etc.

Processed data consists of information over n days.

DATA = [ day_info[0], day_info[2], ..., day_info[n] ]

On the nth day, we stop looking at trend data, and invest in the stock at the open price. ie. open_price[n+1]

We hold the stock for d days, selling at the close price. ie. close_price[n+d]

If we made a profit the data is tagged 1.0, else it's taged 0.0

TAG = 1.0

# DATA LEVEL 0

DATA = [ open_price[0], close_price[0], ..., open_price[n], close_price[n] ]

# DATA LEVEL 1

On each day there's a percentage change, calculated as change[n] = [ (open[n]-close[n]) * (100/close[n]) ]

DATA = [ change[0], change[1], change[2] ... ]

# DATA LEVEL 2

Simple Moving Average 200 is the average of the high prices for the preceding 200 days.

DATA = [ SMA200[0], SMA200[1], ..., SMA200[n] ]

# DATA LEVEL 3

Simple Moving Average 10 is the average of the high prices for the preceding 10 days.

DATA = [ SMA10[0], SMA10[1], ..., SMA10[n] ]
