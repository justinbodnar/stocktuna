# PROPOSED DATA SET ARCHITECTURE

QUESTION: How wo we create a data set to train on historical trends?

	- using monte carlo simulations of course!
	- create random investments on random days in history
	- calculate the resulting delta
	- 1 data point = 1 investment

DATA SET level 0 - least amount of information

	- we're asking the question:
	- 'Considering the past n days of price changes, can this be a good investment?'
	- data point contains:
		- n days of closing price history
                        - double[2*n] of [ open_1, close_1, open_2, close_2, ...., open_n, close_n ]
                        - where day_n is the day before date_bought
	- tag contains:
		- boolean: delta > 0
	- ie. Invest $100 into Rite Aid on Christmas, sold for $105 2 days later would create the following data_point and tag
		- data_point = [ open_1, close_1, open_2, close_2 ]
		- tag        = [ true ]

DATA SET level 1 - moderate amount of information

	- we're taking a time based risk, like range trading
	- we're asking the question:
	- 'Considering the past n days of price changes, should I invest for x days?'
	- data point contains:
		- time delta, in days the shares were held
		- n days of of open/close data as:
			- double[2*n] of [ open_1, close_1, open_2, close_2, ...., open_n, close_n ] 
			- where day_n is the day before date_bought
	- tag contains:
		- boolean: delta > 0
	- ie. Invest $100 into Rite Aid on Christmas, sold for a $5.00 PROFIT 2 days later would create the following data_point and tag
		- data_point = [ 2, open_1, close_1, open_2, close_2 ]
		- tag        = [ true ]

DATA SET level 2 - all information available in yahoo finance api

	- the most information available from the api is:
		- n previous days' data including:
			- Open
	                - High
	                - Low
	                - Close
	                - Adj Close
	                - Volume
	- we're asking the question:
	- 'Considering all available information, should I invest for x days?'
	- data point contains all lists flattened along the rows:
		- [ days_held,
		  open_1, open_2, ..., open_n,
		  high_1, high_2, ..., high_n,
		  low_1, low_2, ..., low_n,
		  close_1 close_2, ..., close_n,
		  adjc_1, adjc_2, ..., adj_n,
		  vol_1, vol_2, ..., vol_n ]
	- tag contains:
		- boolean: delta > 0

# Stonks.py functions defined

def random_dates():

	- returns two random dates; date_1 and date_2
	- date_2 is (1-30) days after date_1
	- format: YYYY-MM-DD

def random_investment( level, n ):

	- random_investment function
	- where level denotes which data level to produce data points for
	- and n is how many days of history to include
	- investments < 30 days, randomized length of time
	- returns data point asa a 1D list of doubles
	- uses yahoo finance api
	- assumes bought at open price
	- and sold at close price
	- example usage; we want a level 2 data point focusing on 30 days of stock history
		- data_point = random_investment( 2, 30 )
		- print( data_point )

# DATA PROCESSING

yf.download( ticker, startdate, enddate )

	- returns a pandas DataFrame object indexed by dates, columns are
		- Open
		- High
		- Low
		- Close
		- Adj Close
		- Volume

	- dates are formatted YYY-MM-DD

	- so to grab Rite Aid's month of February 2018 and print the first day's opening price:
		- data = yf.download('RAD','2018-02-01','2018-02-28')
		- price = data["Open"]["2018-02-01"]
		- print( price )
