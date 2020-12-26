"""
An example library and CLI app using Stock Tuna. Create datasets, classification models, and predictions in historical stock market trends

Functions:

	random_investment(int, int, int, boolean) -> string, 2dlist[string], list[string], float
	create_data_set(int, int, int, int) -> 2dlist[string], list[float]
	graph_data_set(string, 2dlist["string"], list[string], int, int, int, float)
        cli_choose_model( ) -> string, int, int, int, int, int, int, int
        cli_choose_dataset( ) -> string, int, int, int, int
	cli_make_predictions( ) -> int, int, int, int, int
	main( ) 

Misc variables:

    errors
"""
# imports
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import stocktuna as tuna
import tensorflow as tf
import numpy as np
import random
import pickle
import keras
import os

# config
errors = True

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
		processed_history = tuna.simple_moving_average( close_prices, 10 )

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
		processed_history = tuna.simple_moving_average( close_prices, 50 )

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
		processed_history = tuna.simple_moving_average( close_prices, 200 )

	################
	# data level 5 #
	################
	elif level == 5:

		# output
		if verbose:
			print( "data level 5 is EMA10[0], EMA10[1], ...." )

		# get close prices
		close_prices = []
		for candle in raw_history:
			close_prices.append( candle.split(",")[2] )

		# create historical dataset
		smoothing = 2.0 / ( float(n) + 1.0 )
		processed_history = tuna.exponential_moving_average( close_prices, 10, smoothing )

	################
	# data level 6 #
	################
	elif level == 6:

		# output
		if verbose:
			print( "data level 6 is EMA50[0], EMA50[1], ...." )

		# get close prices
		close_prices = []
		for candle in raw_history:
			close_prices.append( candle.split(",")[2] )

		# create historical dataset
		smoothing = 2.0 / ( float(n) + 1.0 )
		processed_history = tuna.exponential_moving_average( close_prices, 50, smoothing )

	################
	# data level 7 #
	################
	elif level == 7:

		# output
		if verbose:
			print( "data level 7 is EMA200[0], EMA200[1], ...." )

		# get close prices
		close_prices = []
		for candle in raw_history:
			close_prices.append( candle.split(",")[2] )

		# create historical dataset
		smoothing = 2.0 / ( float(n) + 1.0 )
		processed_history = tuna.exponential_moving_average( close_prices, 200, smoothing )


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
			if errors:
				print( e )
				print(tuna.print_exception())
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

###############
# main method #
###############
def main():

	global errors

	# print opening header
	print()
	tuna.print_tuna()
	print( "\nstocktuna by Justin Bodnar\n" )
	print( "Can we teach computers to speculate?\n" )

	# main program infinite loop
	choice = 420
	while int(choice) > 0:
		choice = 0

		# main menu text
		print( "Menu" )
		print( "0. EXIT" )
		print( "1. Create new data sets" )
		print( "2. Extend data set" )
		print( "3. List and analyze available data sets" )
		print( "4. Train a model on a data set" )
		print( "5. View a random data point and tag" )
		print( "6. Graph a random data point and tag (uses MatPlotLib)" )
		print( "7. Watch a model make 10,000 predictions" )

		# get user chice
		choice = int(input( "\nEnter choice: "))

		# EXIT
		if choice == 0:
			print( "\nEXITING\n" )
			exit()

		# choice == 1
		# create new data set
		elif choice == 1:

			# get user parameters
			level = int(input("Enter data level: "))
			size = int(input("Enter size of dataset: "))
			n = int(input("Enter the number of days to look at: "))
			d = int(input("Enter number of days invested: "))
			filename = str(level)+"-"+str(size)+"-"+str(n)+"-"+str(d)

			# create data set
			data, tags = create_data_set(level, size, n, d)

			# output
			print( "Dataset saved as ./datasets/"+ filename+"_tags and ./datasets/"+ filename+"_data" ) 
			print( "Filename: level-size-n-d_[data|tags]" )
			# wait for user  input
			pause = input( "Press enter to continue" )

		# choice == 2
		# extend a data set
		elif choice == 2:

			# try-catch block
			try:
				# get user input
				dataset_filename, level, size, n, d = cli_choose_dataset()

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
				newData, newTags = create_data_set(int(level), number_of_data_to_add, int(n), int(d))

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
					print(tuna.print_exception())
				pass

		# choice == 3
		# analyze available data sets
		elif choice == 3:

			# get user input
			dataset_filename, level, size, n, d = cli_choose_dataset()

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
				print( "\nName: ", dataset_filename )
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
					print(print_exception())
				pass

			print()

			# wait for user to press enter
			pause = input( "Press enter to continue." )

		# choice == 4
		# build model from data set
		elif choice == 4:

			# try to unpickle data set and train classifier
			try:

				# get user input
				dataset_filename, level, size, n, d = cli_choose_dataset()

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
					print(tuna.print_exception())
				pass

			# pause for user input
			pause = input( "Press enter to continue" )

		# choice == 5
		# grab and view random datum
		elif choice == 5:
			level = int(input("\nEnter data level: "))
			n = int(input("Enter number of days to look at before investing: "))
			d = int(input("Enter number of days to have been invested: "))
			random_investment( level, n, d, True )

		# choice == 6
		# build model from data set
		elif choice == 6:
			level = int(input("\nEnter data level: "))
			n = int(input("Enter number of days to look at before investing: "))
			d = int(input("Enter number of days to have been invested: "))
			stock_ticker, data, dates, tag = random_investment( level, n, d, False )
			graph_data_set( stock_ticker, data, dates, level, n, d, tag )

		# choice == 7
		# watch model make predictions
		elif choice == 7:

			# get model choice
			model_filename, level, size, n, d, layer1, layer2, layer3 = cli_choose_model()

			# get how many predictions
			count = int(input( "How many predictions to make? "))

			# check for no models
			if level < 0:
				standyby = input( "NO MODELS TO LOAD. PRESS ENTER TO CONTINUE" )
				continue

			cli_make_predictions( count, model_filename, level, n, d )

		# choice != VALID
		else:
			pause = input("Invalid choice\nPress enter to continue.")
main()

