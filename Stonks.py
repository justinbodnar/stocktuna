####################
# Stonk.py         #
# by Justin Bodnar #
####################
import matplotlib.pyplot as plt
import yfinance as yf
import random

# random dates function
# format: YYYY-MM-DD
def random_dates():

	m = random.randrange(12)
	if m == 0:
		d = 32
	elif m == 1:
		d = 28
	elif m == 2:
		d = 31
	elif m == 3:
		d = 30
	elif m == 4:
		d = 29
	elif m == 5:
		d = 30
	elif m == 6:
		d = 31
	elif m == 7:
		d = 31
	elif m == 8:
		d = 30
	elif m == 9:
		d = 30
	elif m == 10:
		d = 30
	elif m == 11 :
		d = 31

	y = random.randrange(2010,2019)

	# casting as strings
	y = str(y)
	m += 1
	if m > 9:
		m = str(m)
	else:
		m = "0" + str(m)
	if d < 10:
		d = "0"+str(d)
	else:
		d = str(d)
	datestamp = y+"-"+m+"-"+d

	# inc month
	if int(m) == 12:
		m = "01"
	else:
		m = str( int(m)+1 )

	# random day
	d = str(random.randrange(28))

	datestamp2 = y+"-"+m+"-"+d

	# return datestamp
	return datestamp, datestamp2

# random_investment function
# takes a stock, date_bought, amount_invested, date_sold
# returns float of delta
# uses yahoo finance api
# assumes bought at open price
# and sold at close price
def random_investment( stock, amount_invested ):

	# get random dates
	date_bought, date_sold = random_dates()

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
	print( "Bought " + str(amount_invested) + " on " + date_bought )
	print( "Sold on " + date_sold + " for a total of " + str(round(sold,2)) )

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
		delta = random_investment( stock, 100.0 )
		print( "Delta: " + str(round(delta,3)) )

	except Exception as e:

		# do nothing
		x = 420

#delta = investment( "RAD", "2018-02-01", "2018-02-28", 1000 )
#print( "Delta: " + str(round(delta,3)) )

randomdate = random_date()
print(randomdate)
