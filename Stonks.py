####################
# Stonk.py         #
# by Justin Bodnar #
####################
import matplotlib.pyplot as plt
import yfinance as yf
import random
import time
import signal
import sys
from datetime import datetime, timedelta

# helper class to suppress random errors
class DevNull:
	def write(self, msg):
		pass

# set stderr to redirect to helper class
sys.stderr = DevNull()

# global stock list
stocks = [ "ACB", "F", "GE", "MSFT", "GPRO", "FIT", "AAPL", "PLUG", "AMD","SNAP", "CRON", "CGC", "HEXO", "TSLA", "FB", "BABA", "CHK", "UBER", "ZNGA", "NIO", "TWTR", "BAC", "AMZN", "T", "S", "APHA", "RAD", "SBUX", "NVDA", "NFLX", "SPCE", "VSLR", "SQ", "KO" ] 


# n days before function
# takes as input n, and a datestamp in format YYYY-MMM-DDD
# returns datestamp n days before
def nDaysBefore( n, d ):

	d = datetime.strptime(d[2:],"%y-%m-%d")
	d = d - timedelta(days=n)
	d = str(d)[:10]

	# return datestamp
	return d

# signal handler funct
def signal_handler(sgnum, frame):
	raise Exception("Timed out!")

# random dates function
# format: YYYY-MM-DD
def random_dates():

	# grab a random month
	m = random.randrange(12)

	# determine how many days are in the random month
	if m == 0:
		d = 32
	elif m == 1:
		d = 28
	elif m == 4:
		d = 29
	elif m == 6 or m == 7 or m == 11 or m == 2:
		d = 31
	elif m == 3 or m == 5 or m == 8 or m == 9 or m == 10:
		d = 30

	# grab a random year
	y = random.randrange(2015,2019)

	# casting as strings
	y = str(y)
	m += 1

	# padding months
	if m > 9:
		m = str(m)
	else:
		m = "0" + str(m)
	if d < 10:
		d = "0"+str(d)
	else:
		d = str(d)
	datestamp = y+"-"+m+"-"+d

	# start on second date
	# should be < 30 days per investment

	# inc month
	if int(m) == 12: # for christmas time investments i guess
		m = 1
		y = str( int(y)+1 )
	else:
		m = int(m)+1

	# padding month
	if m < 10:
		m = "0"+str(m)
	else:
		m = str(m)

	# random day
	d = random.randrange(27)+1

	# padding day
	if d < 9:
		d = "0"+str(d)
	else:
		d = str(d)

	# concat second datestamp string
	datestamp2 = y+"-"+m+"-"+d

	# return datestamps
	return datestamp, datestamp2

# random_investment function
# takes level, and n
# where level is which data level to produce
# and n is number of days in history to look at
# returns a datapoint of a 1D list
# uses yahoo finance api
# assumes bought at open price
# and sold at close price
def random_investment( level, n ):

	# amount_invested is arbitrary
	amount_invested = 100.0

	# whole thing goes in a while loop until completed
	complete = False
	while not complete:

		# try-catch block
		try:

			# get random stock from global list of stocks t o train on
			stock = stocks[random.randrange(len(stocks))]

			# start timer
			signal.signal(signal.SIGALRM, signal_handler)
			signal.alarm(1) # in seconds

			# get random date
			date_bought, date_sold = random_dates()

			# get the data set from yahoo finace api
			data = yf.download( stock, date_bought, date_sold )

			# get opening price
			open = float(data["Open"][date_bought])

			# get closing price
			close = float(data["Close"][date_sold])

			# calculate percentage change
			change = close/open

			# calculate sold price
			sold = amount_invested * change

			# calculate delta
			delta = sold - amount_invested

			# get n days of history
			historyStartDatestamp = nDaysBefore( n, date_bought )
			history = yf.download(stock,historyStartDatestamp,date_bought)

			# build data_point
			# level 0:
			#	- n days of open/close history
			# level 1:
			#	- time delta
			#	- n days of open/close history
			# level 2:
			#	- time delta
			#	- n days of open
			#	- n days of high
			#	- n days of low
			#	- n days of close
			#	- n days of adjusted close
			#	- n days of volume
#			data_point = []
#			if level == 0:
				

			# output
			print( "History starts on", historyStartDatestamp )
			print( "Purchase happens on", date_bought )

			# if we made it this far, functions completed
			complete = True

		# just disregard errors
		except Exception as e:
			pass

	# return delta
	return delta

# lets get a few random trades and see how we make out
# each investment will be $100.00
i = 0
while i < 3:
	i += 1
	print( "Iteration", i )

	try:
		data_point = random_investment( 0, 30 )
		print( data_point )

	except Exception as e:

		print(e)
		# do nothing
		pass

#d = datetime.today() - timedelta(days=3)
#print("datetime trunc:")
#d = str(d)[2:10]
#print(d)
#d = datetime.strptime(d,"%y-%m-%d")
#d = d - timedelta(days=3)
#print("datetime recast:")
#print(d)
