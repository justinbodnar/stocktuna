####################
# Stonks.py        #
# by Justin Bodnar #
####################
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
import pickle
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
stocks = [ "ACB", "F", "GE", "MSFT", "GPRO", "FIT", "AAPL", "PLUG", "AMD","SNAP", "CRON", "CGC", "TSLA", "FB", "BABA", "CHK", "UBER", "ZNGA", "NIO", "TWTR", "BAC", "AMZN", "T", "APHA", "RAD", "SBUX", "NVDA", "NFLX", "SPCE", "VSLR", "SQ", "KO" ] 


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
# takes level, n, and d
# where level is which data level to produce
# n is number of days in history to look at
# d is number of days invested
# returns a datapoint of a 1D list
# uses yahoo finance api
# assumes bought at open price
# and sold at close price
def random_investment( level, n, d ):

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
			signal.alarm(5) # in seconds

			# get random date
			date_bought, date_sold = random_dates()

			# make the date_bought n days before date_sold
			date_bought = nDaysBefore( d, date_sold )

			# get the delta from yahoo finace api
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
			historyStopDatestamp = nDaysBefore( 2, date_bought)
			historyStartDatestamp = nDaysBefore( n, date_bought )
			history = yf.download(stock, historyStartDatestamp, nDaysBefore( 1, date_bought ) )

#			print(history)
#			print("history starts on", historyStartDatestamp, "and ends on", historyStopDatestamp )
#			print("for a size of", len(history))
#			print("purchase made on", date_bought, "for", amount_invested)
#			print("sold on", date_sold, "for", sold)

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

			# add extra days of history if YF is being gay
			sentry = 0
			while len(history) < n:
#				print( "Adding more history to current size of", len(history) )
				sentry = sentry + 1
				if sentry > 30:
					raise Exception("YF API is returning crazy small data rn" )
				historyStartDatestamp = nDaysBefore( sentry, historyStartDatestamp )
				history = yf.download( stock, historyStartDatestamp, historyStopDatestamp )

			# check for invalid history downloads
			if( len(history) < n ):
#				print( "history:", len(history) )
#				print( "n:", n )
#				print( "API RETURNED NOT ENOUGH HISTORY" )
				raise Exception("YF API returned incorrect data")


#			print( "data level:", level )
			# both level 0 and 1 require the open/close chain structure, so start here
			level = int(level)
			if level == 0 or level == 1:

				# creating list of open/close requires casting as iterable list
				openhistory = []
				closehistory = []
				data_point = []
				for each in history["Open"]:
					openhistory.append(each)
				for each in history["Close"]:
					closehistory.append(each)
				for i in range( len(openhistory) ):
					data_point += [ np.float16(round(openhistory[i],2)), np.float(round(closehistory[i],2)) ]

				# if we made it this far, functions completed
#				print( "Completed one datum" )
				complete = True
				return data_point, tag

			# if were level 1 we need to add time elta to front of data point
			if level is 1:
				print( "Level 1 TBA" )
			elif level is 2:
				print( "Level2 TBA" )

		# just disregard errors
		except Exception as e:
#			print(e)
			pass

	# return delta
	return data_point, tag

# createDataSet function
# uses random_investment function
# level number of data level
# size is the size of dataset
# n number of days to look at historically before investing
# d number of days to stay invested
# and n is number of days in history to look at
# returns 2 lists: data, tags
def createDataSet(level, size, n, d):

	# setup vars
	data = []
	tags = []

	# lets get a few random trades and see how we make out
	# each investment will be $100.00
	i = 0
	while len(data) < size and i < 1000:

		print( "[", i+1, "of", size, "]" )
		i = i + 1

		try:
			data_point, tag = random_investment( level, n, d )
			data.append( data_point )
			tags.append( tag )

		except Exception as e:
#			print(e)
			pass

	return data, tags


###############
# main method #
###############
def main():

	# clear the screen
	for i in range(30):
		print()

	# main infinite loop of program
	choice = 420
	while choice > 0:

		print( "##########################" )
		print( "Stonks.py by Justin Bodnar" )
		print()
		print( "Can we teach computers to speculate?" )
		print()
		print( "Menu" )
		print( "1. Create new data sets" )
		print( "2. Analyze current data sets" )
		choice = int(input( "Enter choice: "))

		# choice == 1
		if choice == 1:

			# get user parameters
			filename = input("Data set name: ")
			level = int(input("Enter data level: "))
			sizeOfDataset = int(input("Enter size of dataset: "))
			daysOfHistory = int(input("Enter the number of days to look at: "))
			daysInvested = int(input("Enter number of days invested: "))

			# create data set
			data, tags = createDataSet(level, sizeOfDataset, daysOfHistory, daysInvested)

			# pickle data list in datasets dir
#			with open( "./datasets/"+filename+"_data", "w+" ) as f:
#				f.dump(data,f)
			# pickle tag list in datasets dir
#			with open( "./datasets/"+filename+"_tags", "w+" ) as f:
#				f.dump(tags,f)

			pickle.dump( data, open( "./datasets/"+filename+"_data", "wb" ) )
			pickle.dump( tags, open ( "./datasets/"+filename+"_tags", "wb" ) )

			print( "Dataset save as ./datasets/", filename+"_tags and ./datasets/", filename+"_data" ) 


		# choice == 2
		elif choice == 2:
			print("Choice 2 TBA")
		# choice != VALID
		else:
			print("Invalid choice")
main()

