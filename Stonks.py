####################
# Stonks.py        #
# by Justin Bodnar #
####################
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
from random import *
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

# global var for debugging
errors = True

# helper class to suppress random errors
class DevNull:
	def write(self, msg):
		pass

# set stderr to redirect to helper class
#sys.stderr = DevNull()

# PrintException() funct
# to print a more verbose error message
def PrintException():
	global errors
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	if errors:
		print( 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )

stocks = []
f = open("stonks.txt","r")
for line in f:
	stocks.append(line.strip())

# signal_handler() funct
def signal_handler(sgnum, frame):
	global errors
	if errors:
		raise Exception("Timed out!")

# random_date() funct
# format: YYYY-MM-DD
def random_date():
	min_year = 2000
	max_year=datetime.now().year
	# generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
	start = datetime(min_year, 1, 1, 00, 00, 00)
	years = max_year - min_year + 1
	end = start + timedelta(days=365 * years)
	return str(start + (end - start) * random.random())[:10]

# get_stock_history() funct
# takes stock, level, n
# where stock is the stock to look at
# level is which data level to produce
# n is number of days in history to look at
# returns a datapoint of a 1D list
# uses yahoo finance api
def get_stock_history( stock, level, n ):

	global errors

	# initial data_point and tag
	data_point = []

	# get random stock
	stocks = os.listdir( "./kaggle_stock_dataset/Stocks/" )
	stock = random.choice( stocks )

	print( stock )


# random_investment() funct
# takes level, n, d, and verbose boolean
# where level is which data level to produce
# n is number of days in history to look at
# d is number of days invested
# returns a datapoint of a 1D list
# uses yahoo finance api
# assumes bought at open price
# and sold at close price
def random_investment( level, n, d, verbose ):

	# for errors
	global errors

	# initial data_point and tag
	data_point = []
	tag = -1

	# casting to avoid type errors
	level = int(level)
	n = int(n)
	d = int(d)

	# pick random stock file
	stock_files = os.listdir( "./kaggle_stock_dataset/Stocks" )
	stock_file = stock_files[random.randint(0,len(stock_files))]

	# output
	if verbose:
		print( "\nRandom stock file: " + stock_file )

	# open stock file and convert to list
	f = open( "./kaggle_stock_dataset/Stocks/" + stock_file )
	lines = [line for line in f.readlines()]

	# data level 0
	if level == 0:

		# data level 0 is open[0], close[0], open[1], close[1], ...

		# get total number of days for raw history
		num_of_days = n + d

		# pick random date and calculate the rest
		start = random.randint(1,len(lines)-num_of_days)
		investment_date = start + n
		sold_date = investment_date + d		

		# grab raw history from txt file
		raw_history = []
		for i in range( start, sold_date ):
			raw_history.append( lines[i].strip() )		

		# create historical dataset
		processed_history = []
		for i in range( 0, n ):
			processed_history.append( raw_history[i].split(",")[1] )
			processed_history.append( raw_history[i].split(",")[4] )

		# get data tag
		bought_price = raw_history[n].split(",")[1]
		sold_price = raw_history[len(raw_history)-1].split(",")[4]
		tag = sold_price > bought_price

		# output
		if verbose:
			print( "\n" + str(num_of_days) + " days of Raw history" )
			print( "Date,Open,High,Low,Close,Volume,OpenInt" )
			for entry in raw_history:
				print( entry )
			print( "\n" + str(n) + " days of history to study" )
			print( "[ open[0], close[0], open[1], close[1], ... ]" )
			print( processed_history )
			print( "\nInvestment bought for $" + str(bought_price) )
			print( "Sold for $" + str(sold_price) )
			print( "Good investment: " + str(tag) )

		# return
		return processed_history, tag

	# data level 1
	elif level == 1:
		print( "Level 1 TBA" )

	# data level 2
	elif level == 2:
		print( "Level 2 TBA" )

	# data level invalid
	else:
		if errors:
			print( "Invalid data level. Exiting..." )
		exit()


# createDataSet() funct
# uses random_investment function
# level number of data level
# size is the size of dataset
# n number of days to look at historically before investing
# d number of days to stay invested
# and n is number of days in history to look at
# returns 2 lists: data, tags
def createDataSet(level, size, n, d):

	global errors

	# setup vars
	data = []
	tags = []

	# lets get a few random trades and see how we make out
	# each investment will be $100.00
	i = 0
	while len(data) < size:

		# print output
		print( "[", i+1, "of", size, "]" )
		i = i + 1

		# try to extract a random data point
		try:
			data_point, tag = random_investment( level, n, d )
			data.append( data_point )
			tags.append( tag )

		# print errors:
		except Exception as e:
			if errors:
				print( e )
				PrintException()
			pass

	# return the data and tags lists
	return data, tags


###############
# main method #
###############
def main():

	global errors

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
		print( "2. Extend data set" )
		print( "3. List and analyze available data sets" )
		print( "4. Train a model on a data set" )
		print( "5. Grab and view example datum" )
		print( "6. View a random data point and tag" )

		# get user chice
		choice = int(input( "\nEnter choice: "))

		# create new data set
		if choice == 1:

			# get user parameters
			print( "Filename: level-sizeOfDataset-daysOfHistory-daysInvested_[data|tags]" )
			level = int(input("Enter data level: "))
			sizeOfDataset = int(input("Enter size of dataset: "))
			daysOfHistory = int(input("Enter the number of days to look at: "))
			daysInvested = int(input("Enter number of days invested: "))
			filename = str(level)+"-"+str(sizeOfDataset)+"-"+str(daysOfHistory)+"-"+str(daysInvested)
			# create data set
			data, tags = createDataSet(level, sizeOfDataset, daysOfHistory, daysInvested)

			# save data sets
			try:
				pickle.dump( data, open( "./datasets/"+filename+"_data", "wb" ) )
				pickle.dump( tags, open ( "./datasets/"+filename+"_tags", "wb" ) )
			except Exception as e:
				if errors:
					print( "error on data or tag save" )
					print( e )
					PrintException()

			print( "Dataset saved as ./datasets/", filename+"_tags and ./datasets/", filename+"_data" ) 
			print( "Filename: level-sizeOfDataset-daysOfHistory-daysInvested_[data|tags]" )
			# wait f or user  input
			pause = input( "Press enter to continue" )

		# extend a data set
		elif choice == 2:

			# try-catch block
			try:
				print( "Available data sets" )
				# list files in datalist dir
				for file in os.listdir("./datasets"):
					# only look at dataset files
					if "data" not in file:
						continue
					else:
						print( file )
				print( "\nFilename: level-sizeOfDataset-daysOfHistory-daysInvested_[data|tags]" )
				level = int(input("Enter data level: "))
				sizeOfNewDataset = int(input("Enter number of new data points: "))
				daysOfHistory = int(input("Enter the number of days to look at: "))
				daysInvested = int(input("Enter number of days invested: "))

				# unpickle lists
				data = pickle.load( open( "./datasets/"+file+"_data", "rb" ) )
				tags = pickle.load( open( "./datasets/"+file+"_tags", "rb" ) )

				# get new list
				newData, newTags = createDataSet(level, sizeOfNewDataset, daysOfHistory, daysInvested)

				# append lists
				data += newData
				tags += newTags

				# repickle list
				pickle.dump( data, open( "./datasets/"+file+"_data", "wb" ) )
				pickle.dump( tags, open( "./datasets/"+file+"_tags", "wb" ) )

			# print errors
			except Exceptions as e:
				if errors:
					print( e )
					PrintExceptions()
				pass

		# choice == 3
		# analyze available data sets
		elif choice == 3:

			# print header
			print()
			print("\nDatasets available:")

			# list files in datalist dir
			for file in os.listdir("./datasets"):

				# only look at dataset files
				if "data" not in file:
					continue

				# try to unpickle dataset file
				try:
					# unpickle
					data_set = pickle.load( open( "./datasets/"+file, "rb" ) )

					# get length of dim 2
					min = 99999999
					max = -1

					# loop through dim 1, checking each entry alonog dim 2 for size
					for data_point in data_set:

						# check for min or max
						if len(data_point) > max:
							max = len(data_point)
						if len(data_point) < min:
							min = len(data_point)
					# print output
					print()
					print( "Name: ", file )
					print( "Dim 1:", len(data_set) )
					if min == max:
						print( "Dim 2:", min )
					else:
						print( "Data set irregular with bounds (", min, ",", max, ")" )
						print( "Fixing with lower bound", min, "as new dim2 size" )

						# loop through dim 1, creating new dataset of proper dim 2 size
						regularized_data_set = []
						for data_point in data_set:
							regularized_data_set.append( data_point[-min:] )

						# replace the old dataset with the regularized one
						data_set = regularized_data_set

						# get new stats
						min = 999999
						max = -1
						# for each data_point
						for data_point in data_set:
							# check for new min or max
							if len(data_point) < min:
								min = len(data_point)
							if len(data_point) > max:
								max = len(data_point)

						# print new datset stats
						if min == max:
							print( "New dim 2:", min )
							print( "Repickling. Please rerun this function to confirm updates" )
							pickle.dump( data_set, open( "./datasets/"+file, "wb" ) )
						else:
							print( "Data set STILL irregular with bounds (", min, ",", max, ")" )

				# print errors
				except Exception as e:
					if errors:
						print( e )
						PrintException()
					pass

			print( "\nFilename: level-sizeOfDataset-daysOfHistory-daysInvested_[data|tags]" )
			# print newline for pretty output
			print()

			# wait for user to press enter
			pause = input( "Press enter to continue." )

		# choice 4
		# build model from data set
		elif choice == 4:

			# try to unpickle data set and train classifier
			try:
				print( "\nAvailable data sets" )
				# list files in datalist dir
				for file in os.listdir("./datasets"):
					# only look at dataset files
					if "data" not in file:
						 continue
					else:
						print( file )
				print( "\nFilename: level-sizeOfDataset-daysOfHistory-daysInvested_[data|tags]\n" )

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


				print( "Save model? Y or N" )
				choice = input( "\nEnter choice: ")

				if choice is "Y" or choice is "y":
					# save model
					model_json = model.to_json()
					with open( "models/stonk_model.json", "w") as json_file:
						json_file.write(model_json)
					# serialize weights to HDF5
					model.save_weights("models/stonk_model.h5")
					print( "Model saved" )


			# print errors
			except Exception as e:
				if errors:
					print( e )
					PrintException()
				pass

			# pause for user input
			pause = input( "Press enter to continue" )
		# grab and view datum
		elif choice == 5:
			level = int(input("Enter data level: "))
			stock = input("Enter stock to grab: ")
			n = int(input("Enter number of days to look back at: "))
			datum = get_stock_history( stock, level, n )
			print( datum )
		elif choice == 6:
			level = int(input("Enter data level: "))
			n = int(input("Enter number of days to look at before investing: "))
			d = int(input("Enter number of days to have been invested: "))
			random_investment( level, n, d, True )
		# choice != VALID
		else:
			pause = input("Invalid choice\nPress enter to continue.")
main()

