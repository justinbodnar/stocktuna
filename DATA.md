# ABSTRACT

How do we create a data set to train on historical trends?

	- use monte carlo simulations
	- create random investments startting on a random day in history
	- process the trend for n days before investing
	- invest for d days and see if we made a profit by selling on the last day
	- 1 data point = some processed form of the trend over n days
	- 1 tag = 'we made a profit' True or False boolean 

Note: A working model was built by iknowfirst.com using a genetic algorithm and 15 years of trend data. 

(https://iknowfirst.com/artificial-intelligence-stock-market-algorithmic-analysis-of-humans-and-their-behavior)

# DATA SOURCE

Data set can be found at https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs or https://stocktuna.com/datasets/kaggle-stock-etf-dataset.zip

# BASIC DATA ARCHITECTURE

In the kaggle-stock-etf-dataset/stocks directory are 5,885 csv files, each for a different stock ticker. Each line in a ticker file represents one day of data. Each day is a comma seperated string in the format Date, Open, High, Low, Close, Adj Close, and Volume. Dates are formatted YYYY-MM-DD.

Processed data consists of information over n days.

DATA = [ day_info[0], day_info[1], ..., day_info[n] ]

On the nth day, we stop looking at trend data, and invest in the stock at the open price. ie. open_price[n+1]

We hold the stock for d days, selling at the close price on the final day. ie. close_price[n+d]

If close_price[n+d] > open_price[n+1], we made a profit and the data is tagged 1.0, else it's taged 0.0

# DATA LEVEL 0

DATA = [ open_price[0], close_price[0], ..., open_price[n], close_price[n] ]

# DATA LEVEL 1

On each day there's a percentage change, calculated as change[n] = [ (open[n]-close[n]) * (100/close[n]) ]

DATA = [ change[0], change[1], change[2] ... ]

# DATA LEVEL 2

Simple Moving Average 10 is the average of the high prices for the preceding 10 days.

DATA = [ SMA10[0], SMA10[1], ..., SMA10[n] ]

# DATA LEVEL 3

Simple Moving Average 50 is the average of the high prices for the preceding 50 days.

DATA = [ SMA50[0], SMA50[1], ..., SMA50[n] ]

# DATA LEVEL 4

Simple Moving Average 200 is the average of the high prices for the preceding 200 days.

DATA = [ SMA200[0], SMA200[1], ..., SMA200[n] ]

# DATA LEVEL 5

Exponential Moving Average 10 is the smoothing average over the preceding 10 days

equation from https://www.thebalance.com/simple-exponential-and-weighted-moving-averages-1031196

DATA = [ EMA10[0], EMA10[1], ..., EMA10[n] ]

# DATA LEVEL 6

Exponential Moving Average 50 is the smoothing average over the preceding 50 days

DATA = [ EMA50[0], EMA50[1], ..., EMA50[n] ]

# DATA LEVEL 7

Exponential Moving Average 200 is the smoothing average over the preceding 200 days

DATA = [ EMA200[0], EMA200[1], ..., EMA200[n] ]

# DATA LEVEL 8

Moving Average Convergance Divergance (MACD) is.... just Google it. The equation used is: 

MACD[n] = EMA26[n] - EMA12[n]

DATA = [ MACD[0], MACD[1], ... ]
