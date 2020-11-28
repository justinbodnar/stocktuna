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
import linecache
import sys
import tensorflow as tf
import keras
import numpy as np
import os

# global var for debugging
errors = True

########################################
# DevNull class
# helper class to suppress random errors
class DevNull:
	def write(self, msg):
		pass

# set stderr to redirect to helper class
#sys.stderr = DevNull()

#######################################
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

##############################
# choose_model function
# lists the models in ./models
# asks the user to choose
# returns list containing:
# string relative filepath
# int level
# int size
# int n
# int d
# (returns [-1,-1,-1,-1] if there are no models)
def choose_model( ):
		# print header
		print("\nModels available:")
		# print headers to make data useful
		print( "No.	Level	Size	n	d	layer1	layer2	layer3")
		# create list of files in datalist dir
		models = []
		i = 0
		for file in os.listdir("./models"):
			# append to list of datasets
			models.append( "models/"+ file )
			# print useful information
			print( str(i) + "	" + file.split("-")[0] + "	" + file.split("-")[1] + "	" + file.split("-")[2] + "	" + file.split("-")[3] + "	" + file.split("-")[4] + "	" + file.split("-")[5] + "	" + file.split("-")[6]  ) 
			i += 1

		# check for empty directory
		if i < 1:
			return -1,-1,-1,-1,-1,-1,-1,-1

		# get user input
		model_choice = int(input("\nEnter number of model: ")) 

		# return relative path
		model = models[model_choice]
		return( model, int(model.split("-")[0].split("/")[1]), int(model.split("-")[1]), int(model.split("-")[2]), int(model.split("-")[3]), int(model.split("-")[4]), int(model.split("-")[5]), int(model.split("-")[6])  )

##################################
# choose_dataset function
# lists the datasets in ./datasets
# asks the user to choose
# returns list containing:
# string relative filepath
# int level
# int size
# int n
# int d
# (returns [-1,-1,-1,-1] if there are no datasets)
def choose_dataset( ):
		# print header
		print("\nDatasets available:")
		# print headers to make data useful
		print( "No.	Level	Size	n	d")
		# create list of files in datalist dir
		datasets = []
		i = 0
		for file in os.listdir("./datasets"):
			# only look at dataset files
			if "data" in file:
				# append to list of datasets
				datasets.append( "datasets/"+ file.split("_")[0] )
				# print useful information
				print( str(i) + "	" + file.split("-")[0] + "	" + file.split("-")[1] + "	" + file.split("-")[2] + "	" + file.split("-")[3].split("_")[0] )
				i += 1

		# check for empty directory
		if i < 1:
			return -1,-1,-1,-1,-1
		# get user input
		dataset_choice = int(input("\nEnter number of dataset: ")) 

		# return relative path
		dataset = datasets[dataset_choice]
		return( dataset, int(dataset.split("-")[0].split("/")[1]), int(dataset.split("-")[1]), int(dataset.split("-")[2]), int(dataset.split("-")[3]) )

#############################################
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
	tag = 0

	# casting to avoid type errors
	level = int(level)
	n = int(n)
	d = int(d)

	# pick random stock file
	stock_files = os.listdir( "./kaggle_stock_datasets/Stocks" )
	stock_file = stock_files[random.randint(0,len(stock_files))]

	# output
	if verbose:
		print( "\nRandom stock file: " + stock_file )

	# open stock file and convert to list
	f = open( "./kaggle_stock_datasets/Stocks/" + stock_file )
	lines = [line for line in f.readlines()]

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

	################
	# data level 0 #
	################
	if level == 0:

		# output
		if verbose:
			print( "data level 0 is open[0], close[0], open[1], close[1], ..." )

		# create historical dataset
		processed_history = []
		for i in range( 0, n ):
			processed_history.append( raw_history[i].split(",")[1] )
			processed_history.append( raw_history[i].split(",")[4] )

	################
	# data level 1 #
	################
	elif level == 1:

		# output
		if verbose:
			print( "data level 1 is change[0], change[1], ...." )

		# create historical dataset
		processed_history = []
		for i in range( 0, n ):
			open_price = float( raw_history[i].split(",")[1] )
			sell_price = float( raw_history[i].split(",")[4] )
			change = ( open_price-sell_price ) * ( 100.0 /sell_price )
			processed_history.append( change )
	################
	# data level 2 #
	################
	elif level == 2:

		# output
		if verbose:
			print( "data level 2 is SMA10[0], SMA10[1], ...." )

		# create historical dataset
		processed_history = []
		for i in range( 0, n ):
			# calculate SMA10 for this day
			j = start+i
			summ = 0.0
			for k in range( j-10, j ):
				summ += float(lines[k].split(",")[2])
			processed_history.append( summ/10 )

	################
	# data level 3 #
	################
	elif level == 3:

		# output
		if verbose:
			print( "data level 3 is SMA50[0], SMA50[1], ...." )

		# create historical dataset
		processed_history = []
		for i in range( 0, n ):
			# calculate SMA50 for this day
			j = start+i
			summ = 0.0
			for k in range( j-50, j ):
				summ += float(lines[k].split(",")[2])
			processed_history.append( summ/50 )

	################
	# data level 4 #
	################
	elif level == 4:

		# output
		if verbose:
			print( "data level 4 is SMA200[0], SMA200[1], ...." )

		# create historical dataset
		processed_history = []
		for i in range( 0, n ):
			# calculate SMA200 for this day
			j = start+i
			summ = 0.0
			for k in range( j-200, j ):
				summ += float(lines[k].split(",")[2])
			processed_history.append( summ/200 )

	######################
	# data level invalid #
	######################
	else:
		# output
		if errors and verbose:
			print( "Invalid data level. Exiting..." )
		exit()

	# get data tag
	bought_price = raw_history[n].split(",")[1]
	sold_price = raw_history[len(raw_history)-1].split(",")[4]
	if sold_price > bought_price:
		tag = 1.0
	else:
		tag = 0.0

	# output
	if verbose:
		print( "\n" + str(num_of_days) + " days of Raw history" )
		print( "Date,Open,High,Low,Close,Volume,OpenInt" )
		for entry in raw_history:
			print( entry )
		print( "\n" + str(n) + " days of history to study" )
		print( processed_history )
		print( "\nInvestment bought for $" + str(bought_price) )
		print( "Sold for $" + str(sold_price) )
		print( "Good investment: " + str(tag) )

	# return
	return processed_history, tag

###########################################################
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

		# try to extract a random data point
		try:
			data_point, tag = random_investment( level, n, d, False )
			data.append( data_point )
			tags.append( tag )
			# print output
			print( "[", i+1, "of", size, "]" )
			i = i + 1
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
	while int(choice) > 0:
		choice = 0

		# main menu text
		print()
		print( "Menu" )
		print( "0. EXIT" )
		print( "1. Create new data sets" )
		print( "2. Extend data set" )
		print( "3. List and analyze available data sets" )
		print( "4. Train a model on a data set" )
		print( "5. View a random data point and tag" )
		print( "6. Watch model make a prediction" )

		# get user chice
		choice = int(input( "\nEnter choice: "))

		# EXIT
		if choice == 0:
			print( "\nEXITING\n" )
			exit()

		# create new data set
		elif choice == 1:

			# get user parameters
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

			print( "Dataset saved as ./datasets/"+ filename+"_tags and ./datasets/"+ filename+"_data" ) 
			print( "Filename: level-size-n-d_[data|tags]" )
			# wait for user  input
			pause = input( "Press enter to continue" )

		# extend a data set
		elif choice == 2:

			# try-catch block
			try:
				# get user input
				dataset_filename, level, size, n, d = choose_dataset()

				# check for 0 datasets
				if level < 0:
					print( "NO DATASETS AVAILABLE. BUILD ONE TO CONTINUE." )
					continue

				# get user input
				number_of_data_to_add = int(input("Enter number of data points to add: "))
				size_of_new_dataset = number_of_data_to_add + size

				# unpickle lists
				data = pickle.load( open( dataset_filename + "_data", "rb" ) )
				tags = pickle.load( open( dataset_filename + "_tags", "rb" ) )

				# get new list
				newData, newTags = createDataSet(int(level), number_of_data_to_add, int(n), int(d))

				# append lists
				data += newData
				tags += newTags

				# make new filename
				new_filename = str(level) + "-" + str(size_of_new_dataset) + "-" + str(n) + "-" + str(d)

				# repickle list
				pickle.dump( data, open( "./datasets/"+new_filename+"_data", "wb" ) )
				pickle.dump( tags, open( "./datasets/"+new_filename+"_tags", "wb" ) )

			# print errors
			except Exception as e:
				if errors:
					print( e )
					PrintException()
				pass

		# choice == 3
		# analyze available data sets
		elif choice == 3:

			# get user input
			dataset_filename, level, size, n, d = choose_dataset()

			# check for 0 datasets
			if level < 0:
				print( "NO DATASETS AVAILABLE. BUILD ONE TO CONTINUE." )
				continue

			# try to unpickle dataset file
			try:
				# unpickle
				data_set = pickle.load( open( dataset_filename+"_data", "rb" ) )

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
				print( "Name: ", dataset_filename )
				print( "Dim 1:", len(data_set), "(size)")
				if min == max:
					print( "Dim 2:", min, "(n)" )
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

			print()

			# wait for user to press enter
			pause = input( "Press enter to continue." )

		# choice 4
		# build model from data set
		elif choice == 4:

			# try to unpickle data set and train classifier
			try:

				# get user input
				dataset_filename, level, size, n, d = choose_dataset()

				# check for 0 datasets
				if level < 0:
					print( "NO DATASETS AVAILABLE. BUILD ONE TO CONTINUE." )
					continue

				# get user input
				print( "Using 3-layer neural network" )
				epochs = int(input("Enter number of epochs: "))
				layer1 = int(input("Enter number of nodes for Layer 1: "))
				layer2 = int(input("Enter number of nodes for Layer 2: "))
				layer3 = int(input("Enter number of nodes for Layer 3: "))

				# create model filename
				model_filename = dataset_filename.split("/")[1] + "-" + str(layer1) + "-" + str(layer2) + "-" + str(layer3)

				# unpickle the data and tags lists
				tags = pickle.load( open( dataset_filename+"_tags", "rb" ) )
				data = pickle.load( open( dataset_filename+"_data", "rb" ) )

				# print output
				print("tags initial size:", len(tags))
				print("data initial size:", len(data))

				# split data into training/testing
				size = int( len(data)*(0.75) )
				train_data = np.array( data[1:size] )
				train_tags = np.array( tags[1:size] )
				test_data = np.array( data[size:] )
				test_tags = np.array( tags[size:] )

				# print output
				print("tags training size:", len(train_tags))
				print("data training size:", len(train_data))
				print("tags testing size:", len(test_tags))
				print("data testing size:", len(test_data))

				# train model
				model = keras.Sequential()
				model.add( keras.layers.Dense( layer1, input_dim=len(data[0]) ) )
				model.add( keras.layers.Dense( layer2, input_dim=26 ) )
				model.add( keras.layers.Dense( layer3, input_dim=13 ) )
				model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )
				model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
				model.fit(train_data, train_tags, epochs=epochs)

				# calculate test loss and est acc
				test_loss, test_acc = model.evaluate(test_data, test_tags)

				print('Test accuracy:', test_acc)
				print( "Save model? Y or N" )
				save_choice = input( "\nEnter choice: ")

				if save_choice is "Y" or save_choice is "y":
					# save model
					model.save("./models/"+model_filename)

					# print output
					print( "Model saved" )
					print( "Filename: " + model_filename )
					print( "Filename: level-size-n-d-epochs-layer1-layer2-layer3\n" )

			# print errors
			except Exception as e:
				if errors:
					print( e )
					PrintException()
				pass

			# pause for user input
			pause = input( "Press enter to continue" )

		# grab and view random datum
		elif choice == 5:
			level = int(input("\nEnter data level: "))
			n = int(input("Enter number of days to look at before investing: "))
			d = int(input("Enter number of days to have been invested: "))
			random_investment( level, n, d, True )

		# watch model make a prediction
		elif choice == 6:

			# get model choice
			model_filename, level, size, n, d, layer1, layer2, layer3 = choose_model()

			# check for no models
			if level < 0:
				standyby = input( "NO MODELS TO LOAD. PRESS ENTER TO CONTINUE" )
				continue

			# load model
			model = tf.keras.models.load_model( model_filename )

			# make 10,000 verbose predictions
			right = 0
			wrong = 0
			i = 0
			while i < 10000:
				try:
					print( "\nTest " + str(i) )
					data, tag = random_investment( level, n, d, False )
					data = np.array(data)
					data = data.reshape(1,n)
					prediction = model.predict( data )
					print("Good investment?")
					if prediction[0][0] > prediction[0][1]:
						pred = "Don't invest"
					else:
						pred = "Invest"
					if tag < 1:
						tag = "Don't invest"
					else:
						tag = "Invest"
					print( "Model:  " + pred )
					print( "Actual: " + tag )
					if pred == tag:
						right += 1
					else:
						wrong += 1
					i += 1
#					standby = input( "Press enter for next prediction" )
				# catch errors
				except Exception as e:
#					print( e )
					continue


			print( "\nRight: " + str(right) )
			print( "Wrong: " + str(wrong) )

		# choice != VALID
		else:
			pause = input("Invalid choice\nPress enter to continue.")
main()

