# -*- coding: UTF-8 -*-
"""
Create datasets, classification models, and predictions in historical stock market trends

Classes:

    DevNull

Functions:

	print_tuna( )
	print_exception( ) -> string
	simple_average( list[float] ) -> float
	simple_moving_average( list[floats], int ) -> list[float]
	random_investment(int, int, int, boolean) -> string, 2dlist[string], list[string], float
	create_data_set(int, int, int, int) -> 2dlist[string], list[float]
	graph_data_set(string, 2dlist["string"], list[string], int, int, int, float)
        cli_choose_model( ) -> string, int, int, int, int, int, int, int
        cli_choose_dataset( ) -> string, int, int, int, int
	cli_make_predictions( ) -> int, int, int, int, int

Misc variables:

    errors
"""

# imports
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import linecache
import pickle
import random
import sys
import os

# global var for debugging
errors = True
class DevNull:
	'''
	helper class to suppress random errors
	'''
	def write(self, msg):
		pass

# set stderr to redirect to helper class
#sys.stderr = DevNull()

def print_tuna():
	'''
	Prints an ASCII Tuna
	'''
	print("                              ██                                                        ")
	print("                            ██░░██              ████████                                ")
	print("                          ██░░░░░░████      ████░░░░░░░░██                              ")
	print("                        ██░░░░░░░░░░░░██  ██░░░░░░░░████                        ████    ")
	print("                        ████████████████████░░░░░░██                        ████░░░░██  ")
	print("              ██████████░░░░░░░░░░░░░░░░░░░░████░░██                      ██░░░░░░██    ")
	print("            ██    ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████                  ██░░░░░░██      ")
	print("        ██████  ██  ██░░░░██░░░░░░░░░░░░░░░░░░░░░░░░░░████            ██░░░░░░██        ")
	print("      ██░░░░██      ██░░░░░░██░░░░░░░░████░░░░░░░░░░░░░░░░████        ██░░░░██          ")
	print("    ██░░░░░░░░██████░░░░░░░░██░░░░░░██░░░░██░░░░░░░░░░░░░░░░░░██████████░░░░██          ")
	print("    ██▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░██░░░░██░░░░░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██            ")
	print("      ██░░░░▒▒░░░░░░░░░░░░░░██░░░░░░████░░██░░░░░░░░░░░░░░██████████████░░██            ")
	print("        ██░░░░░░░░░░░░░░░░░░██░░░░░░░░░░██░░░░░░░░░░░░████████        ██░░░░██          ")
	print("          ████░░░░░░░░░░░░██░░░░░░░░░░░░░░░░░░░░░░░░████                ██░░██          ")
	print("              ██████░░░░░░░░░░░░░░░░░░░░░░░░░░██████                    ██░░░░██        ")
	print("                    ██████████░░░░░░░░░░██████░░░░░░██                    ██░░░░██      ")
	print("                      ██░░░░░░██████████    ██░░░░░░░░██                    ██░░░░██    ")
	print("                      ██░░░░░░██              ██░░░░░░░░██                    ██████    ")
	print("                        ██░░░░██                ████████                                ")
	print("                          ██░░██                                                        ")
	print("                            ██                                                          ")

def print_exception():
	'''
	Prints a detailed exception with file names and line numbers.
	'''
	global errors
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	if errors:
		return str('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )

def simple_average( data ):
	'''
	The simple average, or mean, is a number representing a list of numbers. It's calculated as the sum of the numbers divided by the number of values.
		Parameters:
			data(list[float]): data to process
		Returns:
			simple_average(float): the simple average of the data
	'''
	summ = 0.0
	for i in range( len(data) ):
		summ += data[i]
	return summ/len(data)

def simple_moving_average( data, periodicity ):
	'''
	A simple moving average (SMA) calculates the average of a selected range of prices, usually closing prices, by the number of periods in that range.
                Parameters:
			data(list[float]): data to process
                Returns:
                        simple_moving_average(list[float]): the simple moving average of the data for n-periodicity days. last value is the prediction for the day after the data ends
	'''
	# using an associative array to store summs decreases the number of computations by ~75%
	summs = [0] * 2 * len(data)
	sma = []
	# iterate through input data
	for i in range( len(data) ):
		# put this value into the appropriate summs
		# this varies with the periodocity
		for j in range( periodicity ):
			summs[i+j] += float(data[i])
		# check if we should caluclate this number
		if i >= periodicity-1:
			sma.append( summs[i]/periodicity )
	# return comopleted sma
	return sma

def random_investment( level, n, d, verbose ):
	'''
	Gets a single random data point, and processes it

		Parameters:
			level(int): the data level to work with
			n(int): the number of days of history to look at
			d(int): the number of days to hold before selling
			verbose(boolean): whether or not to print what's happening

		Returns:
			ticker(string): the stock ticker that was randomly chosen
			data(2dlist[string]): the datas as CSV strings in a 2d list
			dates(list[string]): the randomly chosen contiguous dates used
			tag(float): the tag, where 1.0 is true, and 0.0 is false
	'''

	# for errors
	global errors

	# initial lists and tag
	data_point = []
	dates = []
	tag = 0

	# casting to avoid type errors
	level = int(level)
	n = int(n)
	d = int(d)

	# pick random stock file
	stock_files = os.listdir( "./kaggle-stock-etf-dataset/stocks" )
	stock_file = stock_files[random.randint(0,len(stock_files))]

	# output
	if verbose:
		print( "\nRandom stock file: " + stock_file )

	# open stock file and convert to list
	f = open( "./kaggle-stock-etf-dataset/stocks/" + stock_file )
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
		dates.append( lines[i].strip().split(",")[0] )

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

		# get close prices
		close_prices = []
		for candle in raw_history:
			close_prices.append( candle.split(",")[2] )

		# create dataset
		processed_history = simple_moving_average( close_prices, 10 )

	################
	# data level 3 #
	################
	elif level == 3:

		# output
		if verbose:
			print( "data level 3 is SMA50[0], SMA50[1], ...." )

		# get close prices
		close_prices = []
		for candle in raw_history:
			close_prices.append( candle.split(",")[2] )

		# create dataset
		processed_history = simple_moving_average( close_prices, 50 )

	################
	# data level 4 #
	################
	elif level == 4:

		# output
		if verbose:
			print( "data level 4 is SMA200[0], SMA200[1], ...." )

		# get close prices
		close_prices = []
		for candle in raw_history:
			close_prices.append( candle.split(",")[2] )

		# create dataset
		processed_history = simple_moving_average( close_prices, 200 )

	################
	# data level 5 #
	################
	elif level == 5:

		# output
		if verbose:
			print( "data level 5 is EMA10[0], EMA10[1], ...." )

		# create historical dataset
		processed_history = []
		last_ema10 = float(lines[start-10].split(",")[2])
		k_constant = 2.0 / ( float(n) + 1.0 )
		for i in range( 0, n ):
			# calculate EMA10 for this day
			j = start+i
			summ = 0.0
			for k in range( j-10, j ):
				summ += float(lines[k].split(",")[2])
			ema10 = summ/10.0
			todays_price = float(lines[j].split(",")[2])
			ema10 = (todays_price-last_ema10) * k_constant + last_ema10
			last_ema10 = ema10
			processed_history.append( ema10 )

	################
	# data level 6 #
	################
	elif level == 6:

		# output
		if verbose:
			print( "data level 6 is EMA50[0], EMA50[1], ...." )

		# create historical dataset
		processed_history = []
		last_ema50 = float(lines[start-50].split(",")[2])
		k_constant = 2.0 / ( float(n) + 1.0 )
		for i in range( 0, n ):
			# calculate EMA50 for this day
			j = start+i
			summ = 0.0
			for k in range( j-50, j ):
				summ += float(lines[k].split(",")[2])
			ema10 = summ/50.0
			todays_price = float(lines[j].split(",")[2])
			ema50 = (todays_price-last_ema50) * k_constant + last_ema50
			last_ema50 = ema50
			processed_history.append( ema50 )

	################
	# data level 7 #
	################
	elif level == 7:

		# output
		if verbose:
			print( "data level 7 is EMA200[0], EMA200[1], ...." )

		# create historical dataset
		processed_history = []
		last_ema200 = float(lines[start-200].split(",")[2])
		k_constant = 2.0 / ( float(n) + 1.0 )
		for i in range( 0, n ):
			# calculate EMA200 for this day
			j = start+i
			summ = 0.0
			for k in range( j-200, j ):
				summ += float(lines[k].split(",")[2])
			ema200 = summ/200.0
			todays_price = float(lines[j].split(",")[2])
			ema200 = (todays_price-last_ema200) * k_constant + last_ema200
			last_ema200 = ema200
			processed_history.append( ema200 )

	################
	# data level 8 #
	################
	elif level == 8:

		# output
		if verbose:
			print( "data level 8 is MACD(12,26)[0], MACD(12,26)[1], ...." )

		# create historical dataset
		processed_history = []
		last_ema26 = float(lines[start-26].split(",")[2])
		last_ema12 = float(lines[start-12].split(",")[2])
		k_constant = 2.0 / ( float(n) + 1.0 )
		for i in range( 0, n ):
			# calculate EMA26 for this day
			j = start+i
			summ = 0.0
			for k in range( j-26, j ):
				summ += float(lines[k].split(",")[2])
			ema26 = summ/26.0
			todays_price = float(lines[j].split(",")[2])
			ema26 = (todays_price-last_ema26) * k_constant + last_ema26
			last_ema26 = ema26
			# calculate EMA12 for this day
			j = start+i
			summ = 0.0
			for k in range( j-12, j ):
				summ += float(lines[k].split(",")[2])
			ema12 = summ/12.0
			todays_price = float(lines[j].split(",")[2])
			ema12 = (todays_price-last_ema12) * k_constant + last_ema12
			last_ema12 = ema12
			# finally, append
			processed_history.append( ema26-ema12 )

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
	return stock_file, processed_history, dates, tag

def create_data_set(level, size, n, d):
	'''
	Creates random data via Monte Carlo simlations, and processes it into a symmetrical dataset for training

		Parameters:
			level (int): the data level to use
			size (int): the size of the dataset
			n (int): the number of trading days processed
			d (int): the number of days before selling

		Returns:
			data (2dlist[string]): training data as 2d list of area SIZE*N
			tags (list[float]): the tags for each data point, associative to data list
	'''
	global errors

	# setup vars
	data = []
	tags = []

	# lets get a few random trades and see how we make out
	i = 0
	while len(data) < size:
		# try to extract a random data point
		try:
			stock_ticker, data_point, dates, tag = random_investment( level, n, d, False )
			data.append( data_point )
			tags.append( tag )

			# print output
			print( "[", i+1, "of", size, "]" )
			i = i + 1

		# print errors:
		except Exception as e:
#			print( e )
			pass

	# save data sets
	try:
		filename = str(level)+"-"+str(size)+"-"+str(n)+"-"+str(d)
		pickle.dump( data, open( "./datasets/"+filename+"_data", "wb" ) )
		pickle.dump( tags, open ( "./datasets/"+filename+"_tags", "wb" ) )
	except Exception as e:
		if errors:
			print( "error on data or tag save" )
			print( e )
			print(print_exception())
	# return the data and tags lists
	return data, tags

def graph_data_set(stock_ticker, data, dates, level, n, d, tags):
	'''
	Uses MatPlotLib to display a visual representation of a dataset (IN DEV)

		Parameters:
			stock_ticker (str): the stock ticker, will be displayed on the graph
			data (2dlist[string]): the data set as 2dstring array of size SIZE*N
			dates (list[string]): the list of dates, associative (am i using this word correctly?) with the data set
			level (int): the data level used
			n (int): the number of days of history per data point
			d (int): the number of days the stock was held before selling
			tags list[float]: list of tags, associative with data set
	'''
	global errors

	# format stock ticker
	stock_ticker = stock_ticker[:stock_ticker.index(".")].upper()

	# start graph
	plt.ylabel("Price")

	# level == 0
	if level == 0:
		# set x ticks and label
		plt.title(stock_ticker + " - Data level " + str(level))
		plt.xlabel( str(n) + " days of data -->" )
		ax = plt.gca()
		xticks = ["0", dates[0]]
		ax.set_xticklabels( xticks )
		# set y ticks and label
		formatter = ticker.FormatStrFormatter('$%1.2f')
		ax.yaxis.set_major_formatter(formatter)
		# create x axis array because native maplotlib function is being a pain
		x = []
		for i in range(2*n):
			x.append( i )
		x = np.array(x)
		# convert strings to floats
		y = []
		for datum in data:
			y.append( float(datum) )
		y = np.array( y )
		plt.plot(x, y)

	# incorrect data level
	else:
		print( "Incorrect data type" )
		return

	# show the plot
	plt.show()

def cli_make_predictions( count, model_filename, level, n, d ):
	'''
	Creates random data points, and lets a model predict the tag

		Parameters:
			count (int): the number of predictions to make
			model_filename (string): the name of the pickled model file
			level (int): the data level to use
			n (int): the number of trading days processed
			d (int): the number of days before selling

	'''
	# load model
	model = tf.keras.models.load_model( model_filename )

	# make verbose predictions
	right = 0
	wrong = 0
	i = 0
	while i < count:
		try:
			print( "\nTest " + str(i) )
			stock_ticker, data, dates, tag = random_investment( level, n, d, False )
			data = np.array(data)
			data = data.reshape(1,n)
			prediction = model.predict( data )
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
#			standby = input( "Press enter for next prediction" )
		# catch errors
		except Exception as e:
			print( e )
			continue


	print( "\nRight: " + str(right) )
	print( "Wrong: " + str(wrong) )


def cli_choose_model( ):
	'''
	Prompts the terminal user to choose an existing model.

		Returns:
			filepath (str): the relative filepath of the chosen model
			level (int): the data level
			size (int): the size of the dataset
			n (int): the number of days of history per data point
			d (int): the number of days the stock was held before selling
	'''
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

def cli_choose_dataset( ):
	'''
	Prompts the terminal user to choose an existing dataset.

		Returns:
			filepath (str): the relative filepath of the chosen dataset
			level (int): the data level
			size (int): the size of the dataset
			n (int): the number of days of history per data point
			d (int): the number of days the stock was held before selling
	'''
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
