####################
# Stonk.py         #
# by Justin Bodnar #
####################
import matplotlib.pyplot as plt
import yfinance as yf
import random
import time
import signal

# signal handler funct
def signal_handler(sgnum, frame):
	raise Exception("Timed out!")

# random dates function
# format: YYYY-MM-DD
def random_dates():

	# this is such an awful naive solution
	# bruteforced rapid typed solution used to save dev time
	# codersdebt++

	# grab a random month
	m = random.randrange(12)

	# determine how many days are in the random month
	if m == 0:
		d = 32
	elif m == 1:
		d = 28
	elif m == 4:
		d = 29
	elif m == 6 or m == 7 or m == 11 or m == 2:
		d = 31
	elif m == 3 or m == 5 or m == 8 or m == 9 or m == 10:
		d = 30

	# grab a random year
	y = random.randrange(2010,2019)

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
# takes a stock
# returns float of delta
# uses yahoo finance api
# assumes bought at open price
# and sold at close price
def random_investment( stock ):

	# amount_invested is arbitrary
	amount_invested = 100.0

	# start timer
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(1) # in seconds

	# get random dates
	date_bought, date_sold = random_dates()

	print( date_bought, date_sold )

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

	# calculate delta
	delta = sold - amount_invested

	# output
	print( "Bought on: " + date_bought + " for a price of: " + str(amount_invested) )
	print( "Sold on:   " + date_sold + " for a total of:   " + str(round(sold,2)) )

	# return delta
	return delta

# lets get a few random trades and see how we make out
# each investment will be $100.00
i = 0
while i < 10:
	i += 1
	print(i)
	stock = "RAD"

	try:
		date1, date2 = random_dates()
		delta = random_investment( stock )
		print( "Delta: " + str(round(delta,3)) )

	except Exception as e:

		# do nothing
		x = 420

#delta = investment( "RAD", "2018-02-01", "2018-02-28", 1000 )
#print( "Delta: " + str(round(delta,3)) )

randomdate = random_dates()
