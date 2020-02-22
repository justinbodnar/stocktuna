####################
# Stonk.py         #
# by Justin Bodnar #
####################
import matplotlib.pyplot as plt
import yfinance as yf

# investment function
# takes a stock, date_bought, amount_invested, date_sold
# returns float of delta
# uses yahoo finance api
# assumes bought at open price
# and sold at close price
def investment( stock, date_bought, date_sold, amount_invested ):

	# first get the data set from yahoo finace api
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

#data = yf.download('RAD','2018-02-01','2018-02-28')
#price = data["Open"]["2018-02-01"]
#print(data)
delta = investment( "RAD", "2018-02-01", "2018-02-28", 1000 )
print( "Delta: " + str(round(delta,3)) )
