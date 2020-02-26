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
import linecache
import sys
import tensorflow as tf
import keras
import numpy as np
import os

# helper class to suppress random errors
class DevNull:
	def write(self, msg):
		pass

# set stderr to redirect to helper class
#sys.stderr = DevNull()

# PrintException() funct
# to print a more verbose error message
def PrintException():

	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print( 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )


# global stock list
stocks = [ "ACB", "F", "GE", "MSFT", "GPRO", "FIT", "AAPL", "PLUG", "AMD","SNAP", "CRON", "CGC", "TSLA", "FB", "BABA", "CHK", "UBER", "ZNGA", "NIO", "TWTR", "BAC", "AMZN", "T", "APHA", "RAD", "SBUX", "NVDA", "NFLX", "SPCE", "VSLR", "SQ", "KO" ] 


# nDaysBefore() funct
# takes as input n, and a datestamp in format YYYY-MMM-DDD
# returns datestamp n days before
def nDaysBefore( n, d ):

	d = datetime.strptime(d[2:],"%y-%m-%d")
	d = d - timedelta(days=n-1)
	d = str(d)[:10]

	# return datestamp
	return d

# signal_handler() funct
def signal_handler(sgnum, frame):
	raise Exception("Timed out!")

# random_dates() funct
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

# random_investment() funct
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
			signal.alarm(15) # in seconds

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

			# build data_point
			# level 0:
			#	- n days of open/close exact history
			# level 1:
			#	- n days of open/close percentage change history
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
				sentry = sentry + 1
				if sentry > 30:
					raise Exception("YF API is returning crazy small data rn" )
				historyStartDatestamp = nDaysBefore( sentry, historyStartDatestamp )
				history = yf.download( stock, historyStartDatestamp, historyStopDatestamp )

			# check for invalid history downloads
#			if( len(history) < n ):
#				raise Exception("YF API returned incorrect data")


			# level 0 requires the open/close chain structure, so start here
			level = int(level)
			if level == 0:

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
				return data_point[(-2*n):], tag

			# if were level 1
			elif level is 1:

				# prepare lists
				data_point = []
				openhistory = []
				closehistory = []

				# grab each day in history
				for each in history["Open"]:
					openhistory.append(each)
				for each in history["Close"]:
					closehistory.append(each)

				# start caluclating percentages
				counter = 0
				lastclose = 0.0
				for each in openhistory:

					# cast each datum
					each = float(each)

					# hack for first element offset in calculating after market hours
					if counter < 1:
						counter = 1
						lastclose = closehistory[0]
						continue

					# calculate percent change from yesterdays close until todays open
					# %change = (new-old)*(100/old)
					change = ( each - lastclose ) * ( 100.0 / lastclose )
					data_point.append(change)
					lastclose = float(closehistory[counter])

					# calculate percent change from todays open until todays close
					# %change = (new-old)*(100/old)
					change = ( float(closehistory[counter]) - each ) * ( 100.0 / each )
					data_point.append( change )

					# increment counter
					counter += 1

				# if we made it this far, functions completed
				return data_point[(-2*n):], tag

			# if were level 2
			elif level is 2:
				print( "Level2 TBA" )

		# just disregard errors
		except Exception as e:
			PrintException()
			pass

	# return delta
	return data_point[(-n*2)+1:], tag

# createDataSet() funct
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

		# print output
		print( "[", i+1, "of", size, "]" )
		i = i + 1

		# try to extract a random data point
		try:
			data_point, tag = random_investment( level, n, d )
			print( "data_point size:", len(data_point) )
			data.append( data_point )
			tags.append( tag )

		# catch exception
		except Exception as e:

			# do nothing
			PrintException()
			pass

	# return the data and tags lists
	return data, tags


###############
# main method #
###############
def main():

	# clear the screen
	for i in range(30):
		print()

	# print opening header
	print( "##########################" )
	print( "Stonks.py by Justin Bodnar" )
	print()
	print( "Can we teach computers to speculate?" )
	print()

	# main program infinite loop
	choice = 420
	while choice > 0:

		# main menu text
		print()
		print( "Menu" )
		print( "1. Create new data sets" )
		print( "2. List and analyze available data sets" )
		print( "3. Train a model on a data set" )

		# get user chice
		choice = int(input( "\nEnter choice: "))

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

			# save data sets
			try:
				pickle.dump( data, open( "./datasets/"+filename+"_data", "wb" ) )
				pickle.dump( tags, open ( "./datasets/"+filename+"_tags", "wb" ) )
			except Exception as e:
				print( "error on data or tag save" )
				PrintException()

			print( "Dataset saved as ./datasets/", filename+"_tags and ./datasets/", filename+"_data" ) 

			# wait f or user  input
			pause = input( "Press enter to continue" )

		# choice == 2
		# analyze available data sets
		elif choice == 2:

			print()
			print("\nDatasets available:")

			# print columns for output
			print( "\nname - count\n" )

			# list files in datalist dir
			for file in os.listdir("./datasets"):

				# only look at dataset files
				if "data" not in file:
					continue

				# try to unpickle dataset file
				try:
					temp = pickle.load( open( "./datasets/"+file, "rb" ) )
					# print length of dataset
					print( file, len(temp) )

				# catch exception
				except Exception as e:
					# do nothing
					PrintException()
					pass

			print()

			# wait for user to press enter
			pause = input( "Press enter to continue." )

		# choice 3
		# build model from data set
		elif choice == 3:

			# try to unpickle data set and train classifier
			try:

				# get user parameters
				filename = input("Enter name of dataset: ")
				print( "Using 3-layer neural network" )
				epochs = int(input("Enter number of epochs: "))
				layer1 = int(input("Enter number of nodes for Layer 1: "))
				layer2 = int(input("Enter number of nodes for Layer 2: "))
				layer3 = int(input("Enter number of nodes for Layer 3: "))

				# unpickle the data and tags lists
				tags = pickle.load( open( "./datasets/"+filename+"_tags", "rb" ) )
				data = pickle.load( open( "./datasets/"+filename+"_data", "rb" ) )

				print("tags initial size:", len(tags))
				print("data initial size:", len(data))

				size = int( len(data)*(0.75) )

				train_data = np.array( data[1:size] )
				train_tags = np.array( tags[1:size] )
				test_data = np.array( data[size:] )
				test_tags = np.array( tags[size:] )


				print("tags training size:", len(train_tags))
				print("data training size:", len(train_data))
				print("tags testing size:", len(test_tags))
				print("data testing size:", len(test_data))


				model = keras.Sequential()
				model.add( keras.layers.Dense( layer1, input_dim=len(data[0]) ) )
				model.add( keras.layers.Dense( layer2, input_dim=26 ) )
				model.add( keras.layers.Dense( layer3, input_dim=13 ) )
				model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )

				model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

				model.fit(train_data, train_tags, epochs=epochs)

				test_loss, test_acc = model.evaluate(test_data, test_tags)

				print('Test accuracy:', test_acc)


				# save model
#				model_json = model.to_json()
#				with open( "models/model.3.json", "w") as json_file:
#					json_file.write(model_json)
				# serialize weights to HDF5
#				model.save_weights("models/blackjackmodel.3.h5")
#				print( "Model saved" )


			# catch exceptions
			except Exception as e:

				# print error
				PrintException()

				# do nothing
				pass

			# pause for user input
			pause = input( "Press enter to continue" )

		# choice != VALID
		else:
			pause = input("Invalid choice\nPress enter to continue.")
main()

