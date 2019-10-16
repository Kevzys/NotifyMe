from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock, StockList
from .forms import CreateNewStockList, CreateNewStock

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from ringcentral import SDK
import requests, json

apikey = '6H75Z4MUU2EOD3H1'
# Create your views here.
def index(response):
    return render(response, "stocks/home.html")

def home(response, id):
    stocklist = StockList.objects.get(id=id)
    if stocklist in response.user.stocklist.all():
        return render(response, "stocks/viewstocklist.html", {"stocklist": stocklist})
    else:
        pass
    return render(response, "stocks/viewlist.html")


# CREATE NEW LIST
def create(response):
    if response.method == "POST":
        form = CreateNewStockList(response.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            stocklist = StockList(name=name)
            stocklist.save()
            response.user.stocklist.add(stocklist)
            return render(response, 'stocks/viewstocklist.html')
    else:
        form = CreateNewStockList()
    return render(response, "stocks/create.html", {"form": form})

#VIEW LIST
def view_list(response):
    return render(response, 'stocks/viewstocklist.html', {})


#DELETE LIST
def removelist(response, id):
    stocklist = StockList.objects.get(id=id)
    if stocklist in response.user.stocklist.all():
        response.user.stocklist.filter(id=id).delete()
        return render(response, 'stocks/viewstocklist.html')



#DELETE STOCK FROM LIST
def removestock(response, id, symbol):
    stocklist = StockList.objects.get(id=id)
    if stocklist in response.user.stocklist.all():
        s = response.user.stocklist.get(id=id)
        s.stock_set.filter(symbol=symbol).delete()
        return render(response, 'stocks/viewstocklist.html')

# ADD STOCK TO LIST
def addToList(response, id):
    stocklist = StockList.objects.get(id=id)
    if stocklist in response.user.stocklist.all():
        if response.method == "POST":
            form = CreateNewStock(response.POST)
            if form.is_valid():
                #call api to get values (should get notification for every list)
                symbol = form.cleaned_data['symbol']
                data = findStock(response, symbol)
                v  = isValid(data)
                if v == True:
                    company = findCompany(symbol)
                    currPrice = parseData(data)
                    valid = 'Added to list'
                    s = response.user.stocklist.get(id=id)
                    s.stock_set.create(company=company, symbol=symbol, price=currPrice)
                    #sendSMS()
                    return render(response, 'stocks/viewstocklist.html')

                else:
                    valid = 'Symbol could not be recognized, try again.'
                    return render(response, 'stocks/addstock.html', {"valid": valid, "form": form})
        else:
            form = CreateNewStock()
        return render(response, 'stocks/addstock.html', {"form": form})
    return

'''
def removeList(response, id):
    stocklist = StockList.objects.get(id=id)
    if stocklist in response.user.stocklist.all():
        StockList.objects.remove(id=id)
        return render(response, 'stocks/viewstockslist.html')
'''

#################### HELPER FUNCTIONS ################
def findStock(response, symbol):


    function = 'TIME_SERIES_INTRADAY'
    interval = '5min'
    call = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&interval=60min' + '&apikey=' + apikey

    data = requests.get(call)
    return data

def parseData(data):
    meta_data_count = 0
    responseJSON = data.json()
    for key1, value1 in responseJSON.items():
        if meta_data_count == 1:
            for key3, value3 in value1.items():
                for key4, value4 in value3.items():
                    if key4 == '4. close':
                        price = value4
                break
        if meta_data_count > 1:
            break
        meta_data_count+= 1

    return price
'''
def parseFirstAndSecondPrice(data):
    meta_data_count = 0
    count = 0
    responseJSON = data.json()
    for key1, value1 in responseJSON.items():
        if meta_data_count == 1:
            for key3, value3 in value1.items():
                if count == 0:
                    for key4, value4 in value3.items():
                        if key4 == '4. close':
                            curr_price = value4
                if count == 1:
                    for key5, value5 in value3.items():
                        if key5 == '4. close':
                            prev_price = value5
                            break
                count +=1
        if meta_data_count > 1:
            break
        meta_data_count+= 1

    percentage_diff = calcDifference(curr_price, prev_price)

    return percentage_diff
'''
def calcDifference(curr_price, prev_price):
        dec = prev_price - curr_price
        percentage_diff = (dec / original) * 100

        return percentage_diff

def isValid(response):
    if response is None:
        return False
    else:
        responseJSON = response.json()
        list_json = list(responseJSON)
        if list_json[0] == 'Error Message':
            return False
        else:
            return True
    return

def findCompany(symbol):
    function = 'SYMBOL_SEARCH'
    keywords = symbol
    call = 'https://www.alphavantage.co/query?function=' + function + '&keywords=' + keywords + '&apikey=' + apikey

    data = requests.get(call)
    dataJSON = data.json()
    count = 0
    x = dataJSON['bestMatches']
    if not x:
        return ''
    y = x[0]
    company = y['2. name']
    return company

##### SEND SMS ##### (CAN USE IN ANY APPLICATION WITH RING CENTRAL API)
def sendSMS():

    RECIPIENT = '16479958354'

    RINGCENTRAL_CLIENTID = 'ytNEYQCjS86w1BIYgIZNng'
    RINGCENTRAL_CLIENTSECRET = 'UU_Bm0yxT0SRaoQy3lSbggUozARI4lRe-6RNuuM1eWig'
    RINGCENTRAL_SERVER = 'https://platform.devtest.ringcentral.com'

    RINGCENTRAL_USERNAME = '+12055824832'
    RINGCENTRAL_PASSWORD = 'Pokemon1029!'
    RINGCENTRAL_EXTENSION = '101'

    rcsdk = SDK( RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
    platform = rcsdk.platform()
    platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)

    platform.post('/restapi/v1.0/account/~/extension/~/sms',
                  {
                      'from' : { 'phoneNumber': RINGCENTRAL_USERNAME },
                      'to'   : [ {'phoneNumber': RECIPIENT} ],
                      'text' : 'Hey gurlllllll'
                  })

################ END HELPER FUNCTIONS ################
