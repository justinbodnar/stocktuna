f = open( "stonks.txt", "r" )
for line in f:
	print( line.split("|")[0] )
