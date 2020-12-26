# -*- coding: UTF-8 -*-
"""
Process stock market data for technical analysis.

Classes:

    DevNull

Functions:

	print_tuna( )
	print_exception( ) -> string
	simple_average( list[float] ) -> float
	simple_moving_average( list[floats], int ) -> list[float]
	exponential_moving_average( list[float], int, float ) -> list[float]

Misc variables:

    errors
"""

# imports
import numpy as np
import linecache
import pickle
import sys

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
	# pad sma array to reflect the lack of calculations on the first input values
	sma = [0] * (periodicity-1)
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

def exponential_moving_average( data, periodicity, smoothing ):
	'''
	Calculates the exponential moving average of the input data set, returning a list
		Parameters:
			data(list[float]): the input data to process
			periodicity(int): the period to process over
			smoothing(float): the alpha to calculate with
		Returns:
			ema(list[float]): the list of ema values
	'''
	# decrease repeat calculations and increase code readability
	p = periodicity
	s = smoothing
	s2 = 1.0 - s
	# first get simple moving average
	sma = simple_moving_average( data, p )
	# to keep code/output readable, keep array associative to input via padding
	ema = [0] * (p-1)
	# start at i = periodicity - 1
	ema.append( s * sma[p-2] + s2 * sma[p-3] )
	# iterate through the rest
	for i in range( periodicity, len(data) ):
		ema.append( s* ema[i-1] + s2 * sma[i-2] )
	# return ema array
	return ema


