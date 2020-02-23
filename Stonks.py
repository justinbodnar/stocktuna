####################
# Stonks.py        #
# by Justin Bodnar #
####################
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
import random
import time
import signal
import sys
import tensorflow as tf
import keras
import numpy as np

# helper class to suppress random errors
class DevNull:
	def write(self, msg):
		pass

# set stderr to redirect to helper class
sys.stderr = DevNull()

# global stock list
stocks = [ "ACB", "F", "GE", "MSFT", "GPRO", "FIT", "AAPL", "PLUG", "AMD","SNAP", "CRON", "CGC", "HEXO", "TSLA", "FB", "BABA", "CHK", "UBER", "ZNGA", "NIO", "TWTR", "BAC", "AMZN", "T", "APHA", "RAD", "SBUX", "NVDA", "NFLX", "SPCE", "VSLR", "SQ", "KO" ] 


# n days before function
# takes as input n, and a datestamp in format YYYY-MMM-DDD
# returns datestamp n days before
def nDaysBefore( n, d ):

	d = datetime.strptime(d[2:],"%y-%m-%d")
	d = d - timedelta(days=n-1)
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
	if m == 1:
		d = 28
	elif m == 4:
		d = 29
	elif m ==0 or m == 6 or m == 7 or m == 11 or m == 2:
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

	# initial data_point and tag
	data_point = []
	tag = -1

	# amount_invested is arbitrary
	amount_invested = 100.0

	# whole thing goes in a while loop until completed
	complete = False
	while not complete:

		# try-catch block
		try:

			# get random stock from global list of stocks t o train on
			stock = stocks[random.randrange(len(stocks))]

			# start timer to catch infinite loops in yf class
			signal.signal(signal.SIGALRM, signal_handler)
			signal.alarm(2) # in seconds

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

			# calculate tag from delta
			delta = sold - amount_invested
			tag = delta > 0

			# get n days of history
			historyStartDatestamp = nDaysBefore( n+1, date_bought )
			history = yf.download(stock, historyStartDatestamp, nDaysBefore( 1, date_bought ) )

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
			historyRaw = yf.download( stock, historyStartDatestamp, nDaysBefore( 2, date_bought ) )

			# check for invalid history downloads
			if(len(historyRaw) < n):
				raise Exception("YF API returned incorrect data")

			# both level 0 and 1 require the open/close chain structure, so start here
			if level is 0 or level is 1:

				# creating list of open/close requires casting as iterable list
				openhistory = []
				closehistory = []
				data_point = []
				for each in historyRaw["Open"]:
					openhistory += [ each ]
				for each in historyRaw["Close"]:
					closehistory += [ each ]
				for i in range( len(openhistory) ):
					data_point += [ np.float16(round(openhistory[i],2)), np.float(round(closehistory[i],2)) ]

				# output
#				print( "History starts on", historyStartDatestamp )
#				print( "Purchase happens on", date_bought )

#				print(historyRaw )

				# if we made it this far, functions completed
				complete = True

			# if were level 1 we need to add time elta to front of data point
			if level is 1:
				print( "Level 1 TBA" )
			elif level is 2:
				print( "Level2 TBA" )

		# just disregard errors
		except Exception as e:
			print(e)
			pass

	# return delta
	return data_point, tag


data = []
tags = []
# lets get a few random trades and see how we make out
# each investment will be $100.00
for i in range(5):

	print( "Iteration", i )

	try:
		data_point, tag = random_investment( 0, 3 )
		data.append( data_point )
		tags.append( tag )
		print( "Added another entry" )

	except Exception as e:

		print(e)
		pass

for i in range( len(data) ):
	print( data[i] )
	print( tags[i] )
