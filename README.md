# PROPOSED DATA SET ARCHITECTURE

QUESTION: How wo we create a data set to train on historical trends?

	- using monte carlo simulations of course!
	- create random investments on random days in history
	- calculate the resulting delta
	- a datum = 1 investment

DATA SET level 0 - least amount of information

	- we're asking the question:
	- 'Considering the past n days of price changes, should I invest, and for how long?'
	- datum contains:
		- n days of closing price history
		- time delta
	- tag contains boolean
		- delta < 0

DATA SET level 1 - moderate amount of information

	- we're taking a time based risk, like range trading
	- datum contains:
		- 
# Stonks.py

def random_dates():

def random_investment( stock, amount_invested ):

	- random_investment function
	- investments < 30 days, randomized length of time
	- takes a stock, and amount_invested
	- returns float of delta
	- uses yahoo finance api
	- assumes bought at open price
	- and sold at close price
	- example usage; we invest $1,000.00 in Rite Aid on a random date
		- delta = investment( "RAD", 1000 )
		- print( "Delta: " + str(round(delta,3)) )

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
