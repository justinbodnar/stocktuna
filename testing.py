import yfinance as yf

data = yf.download('WMT','2020-10-26','2020-11-24')
print( data )
