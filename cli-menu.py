"""
cli-menu.py
by Justin Bodnar
"""

# imports
import stocktuna as tuna
import tensorflow as tf
import numpy as np
import pickle
import keras

# config
errors = True


###############
# main method #
###############
def main():

	global errors

	# print opening header
	print()
	tuna.print_tuna()
	print( "\nstock-tuna by Justin Bodnar\n" )
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
		print( "7. Watch model make a prediction" )

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
			sizeOfDataset = int(input("Enter size of dataset: "))
			daysOfHistory = int(input("Enter the number of days to look at: "))
			daysInvested = int(input("Enter number of days invested: "))
			filename = str(level)+"-"+str(sizeOfDataset)+"-"+str(daysOfHistory)+"-"+str(daysInvested)
			# create data set
			data, tags = tuna.createDataSet(level, sizeOfDataset, daysOfHistory, daysInvested)

			# save data sets
			try:
				pickle.dump( data, open( "./datasets/"+filename+"_data", "wb" ) )
				pickle.dump( tags, open ( "./datasets/"+filename+"_tags", "wb" ) )
			except Exception as e:
				if errors:
					print( "error on data or tag save" )
					print( e )
					print(tuna.print_exception())

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
				dataset_filename, level, size, n, d = tuna.choose_dataset()

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
				newData, newTags = tuna.createDataSet(int(level), number_of_data_to_add, int(n), int(d))

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
			dataset_filename, level, size, n, d = tuna.choose_dataset()

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
				dataset_filename, level, size, n, d = tuna.choose_dataset()

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
			tuna.random_investment( level, n, d, True )

		# choice == 6
		# build model from data set
		elif choice == 6:
			level = int(input("\nEnter data level: "))
			n = int(input("Enter number of days to look at before investing: "))
			d = int(input("Enter number of days to have been invested: "))
			stock_ticker, data, dates, tag = tuna.random_investment( level, n, d, False )
			tuna.graph_data_set( stock_ticker, data, dates, level, n, d, tag )

		# choice == 7
		# watch model make 10,000 prediction
		elif choice == 7:

			# get model choice
			model_filename, level, size, n, d, layer1, layer2, layer3 = tuna.choose_model()

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
					stock_ticker, data, dates, tag = tuna.random_investment( level, n, d, False )
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
					print( e )
					continue


			print( "\nRight: " + str(right) )
			print( "Wrong: " + str(wrong) )

		# choice != VALID
		else:
			pause = input("Invalid choice\nPress enter to continue.")
main()

