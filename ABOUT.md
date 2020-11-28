# ABSTRACT

How do we create a data set to train on historical trends?

	- use monte carlo simulations
	- create random investments on random days in history
	- calculate the trend for n days before investing
	- invest for d days and see if we made a profit
	- 1 data point = some processed form of the trend over n days
	- 1 tag = 'we made a profit' True or False boolean 

Note: A working model was built by iknowfirst.com using a genetic algorithm and 15 years of trend data. 

(https://iknowfirst.com/artificial-intelligence-stock-market-algorithmic-analysis-of-humans-and-their-behavior)

# Stonks.py functions defined

def createDataSet(level, size, n, d):

	- returns two lists: tags, and data
	- tags are booleans
	- data is a single linked list of 32-bit floats
	- takes as input:
	- int level: data level to extract
	- int size: total size of dataset
	- int n: number of days of history before purchase to look at
	- int d: number of days to invest for
	- uses random_investment() for each data point and tag

def random_investment( level, n, d ):

	- return a float tag, and a datum
	- tag is a (0.0 1.0)
	- datum is a linked list of 16-bit floats
	- takes as input:
	- int level: data level to extract
	- int n: number of days of history before purchase
	- int d: number of days before selling the shares
	- assumes bought at open price
	- and sold at close price

def signal_handler(sgnum, frame):

	- helper function to time out infinite loops in yf class

def PrintException():

	- helper function to print stack trace for debugging
