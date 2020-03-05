#######################
# Stonks-v2.py        #
# by Justin Bodnar    #
#######################
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from WorldTradingData import WorldTradingData
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
sys.stderr = DevNull()

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
	y = random.randrange(2009,2019)

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
# assumes bought at open price
# and sold at close price
def random_investment( level, n, d ):

	return 0

# createDataSet() funct
# uses random_investment function
# level number of data level
# size is the size of dataset
# n number of days to look at historically before investing
# d number of days to stay invested
# and n is number of days in history to look at
# returns 2 lists: data, tags
def createDataSet(level, size, n, d):

	return 0


###############
# main method #
###############
def main():

	# clear the screen
	for i in range(30):
		print()

	# print opening header
	print( "#############################" )
	print( "Stonks-v2.py by Justin Bodnar" )
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

		# get user chice
		choice = int(input( "\nEnter choice: "))

		# choice == 1
		if choice == 1:

			print( "TBA" )

main()
