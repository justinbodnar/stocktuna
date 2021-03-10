from auth import *
import stocktuna as tuna
import requests
import json

'''
https://rapidapi.com/apidojo/api/bloomberg-market-and-financial-news?endpoint=
'''

url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-chart"

querystring = {"interval":"y1","id":"wmt:us"}

headers = { 'x-rapidapi-key': rapidapi_key,'x-rapidapi-host': rapidapi_host }

s = requests.request("GET", url, headers=headers, params=querystring).text

# for testing
#s = '{"result":{"WMT:US":{"historical":true,"ticksType":"DayTick","ticks":[{"time":1606831200,"close":152.64,"volume":7647091},{"time":1606917600,"close":150.52,"volume":7849016},{"time":1607004000,"close":149.3,"volume":8575283},{"time":1607090400,"close":148.91,"volume":6963068},{"time":1607349600,"close":148.11,"volume":6159738},{"time":1607436000,"close":149.45,"volume":6905454},{"time":1607522400,"close":148.27,"volume":6713231},{"time":1607608800,"close":147.04,"volume":6884118},{"time":1607695200,"close":147.0,"volume":5620262},{"time":1607954400,"close":145.65,"volume":8362652},{"time":1608040800,"close":145.58,"volume":10631500},{"time":1608127200,"close":145.43,"volume":8550348},{"time":1608213600,"close":146.1,"volume":10226457},{"time":1608300000,"close":145.95,"volume":13794744},{"time":1608559200,"close":145.97,"volume":8517668},{"time":1608645600,"close":144.2,"volume":12554057},{"time":1608732000,"close":143.22,"volume":6810150},{"time":1608818400,"close":143.5,"volume":3018157},{"time":1609164000,"close":145.22,"volume":6448325},{"time":1609250400,"close":144.3,"volume":5979380},{"time":1609336800,"close":144.18,"volume":6250385},{"time":1609423200,"close":144.15,"volume":5938018}],"low":"143.22","high":"152.64","first":1606831200,"last":1609423200,"security":{"ticker":"WMT:US","open":"144.20","prevClose":"152.64"},"hasVolume":true}}}'

j = json.loads(s)

print( j )

data = []
for each in j["result"]["wmt:us"]["ticks"]:
	data.append( each["close"] )

print()
print( "RAW" )
print( data )
print()
print( "Simple Average" )
print( tuna.simple_average( data ) )
print()
print( "Simple Moving Average p=50" )
#print( tuna.simple_moving_average( data, 50 ) )
print( tuna.simple_moving_average( data, 50 )[-1] )
print()
print( "Exponential Moving Average p=50, a=0.003" )
#print( tuna.exponential_moving_average( data, 50, 0.003 ) )
print( tuna.exponential_moving_average( data, 50, 0.003 )[-1] )
print()
