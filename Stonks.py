import matplotlib.pyplot as plt
import yfinance as yf

print("-----------------------")
data = yf.download('RAD','2018-02-01','2018-02-28')
print(data)
print("-----------------------")
price = data["Open"]["2018-02-01"]
print( price )
print("-----------------------")
#print( data["Open"]["2018-01-02"] )
print("-----------------------")
# Plot the close price of the AAPL
#data.Close.plot()
#plt.show()
