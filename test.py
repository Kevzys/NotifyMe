from django.shortcuts import render

call = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPAAAL&apikey=6H75Z4MUU2EOD3H1'
data = response.get(call)
print(call)
