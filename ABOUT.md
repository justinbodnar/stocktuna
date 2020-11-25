# PROPOSED DATA SET ARCHITECTURE

QUESTION: How do we create a data set to train on historical trends?

	- using monte carlo simulations
	- create random investments on random days in history
	- calculate the resulting delta
	- 1 data point = 1 investment
	- all floats cast 16 bit via np.float16()

A working model was built by iknowfirst.com using a genetic algorithm and 15 years of trend data. 

(https://iknowfirst.com/artificial-intelligence-stock-market-algorithmic-analysis-of-humans-and-their-behavior)


Stonks.py Version 1 - use Yahoo Finance API

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
	- 'Considering the past n days of price percentage changes, should I invest for x days?'
	- data point contains:
		- 2 * n days of of open/close percentage change data as:
			- each day of history produces:
			- percentage change during trading hours
			- percentage change after market hours
	- tag contains:
		- boolean: delta > 0


Stonks.py Version 2 - use WorldTradeData API

	- TBA


# Stonks.py functions defined

def createDataSet(level, size, n, d):

	- returns two lists: tags, and data
	- tags are booleans
	- data is a single linked list of 16-bit floats
	- takes as input:
	- int level: data level to extract
	- int size: total size of dataset
	- int n: number of days of history before purchase to look at
	- int d: number of days before selling the shares
	- uses random_investment() for each data point and tag

def random_investment( level, n, d ):

	- return a tag, and a datum
	- tag is a boolean
	- datum is a linked list of 16-bit floats
	- takes as input:
	- int level: data level to extract
	- int n: number of days of history before purchase
	- int d: numebr of days before selling the shares
	- uses yahoo finance api
	- assumes bought at open price
	- and sold at close price

def random_dates():

	- returns two random dates; date_1 and date_2
	- date_2 is (1-30) days after date_1
	- format: YYYY-MM-DD

def nDaysBefore( n, d ):

	- take as input a time delta n, and a string datestamp d
	- returns a datestamp string n days before input datestamp
	- useful for grabbing chunks of stock history

def signal_handler(sgnum, frame):

	- helper function to time out infinite loops in yf class

# DATA PROCESSING

yf.download( ticker, startdate, enddate )

	- returns a pandas DataFrame object indexed by dates, columns are
		- Open
		- High
		- Low
		- Close
		- Adj Close
		- Volume

	- dates are formatted YYYY-MM-DD

	- so to grab Rite Aid's month of February 2018 and print the first day's opening price:
		- data = yf.download('RAD','2018-02-01','2018-02-28')
		- price = data["Open"]["2018-02-01"]
		- print( price )
