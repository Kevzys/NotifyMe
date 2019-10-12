from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock, StockList
from .forms import CreateNewStockList, CreateNewStock
from ringcentral import SDK
import requests, json

apikey = '6H75Z4MUU2EOD3H1'
# Create your views here.
def index(response):
    return render(response, "stocks/home.html")

def home(response, id):
    stocklist = StockList.objects.get(id=id)
    if stocklist in response.user.stocklist.all():
        return render(response, "stocks/list.html", {"stocklist": stocklist})
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
            return render(response, 'stocks/home.html')
    else:
        form = CreateNewStockList()
    return render(response, "stocks/create.html", {"form": form})

def view_list(response):
    print(response.user.stocklist.all())
    return render(response, 'stocks/viewstocklist.html', {})

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
                    sendSMS()
                    return render(response, 'stocks/addstock.html', {"valid": valid, "form": form})

                else:
                    valid = 'Symbol could not be recognized, try again.'
                    return render(response, 'stocks/addstock.html', {"valid": valid, "form": form})
        else:
            form = CreateNewStock()
        return render(response, 'stocks/addstock.html', {"form": form})
    return

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
    print(company)
    return company

def sendSMS():

    RECIPIENT = '16479958354'

    RINGCENTRAL_CLIENTID = '2S1C-6pgQHCoEZ1MUyjp8A'
    RINGCENTRAL_CLIENTSECRET = 'mo-HR_sDQNqZpwfiyVeBEwYchILMcCRv6uBIWZqMqzaQ'
    RINGCENTRAL_SERVER = 'https://platform.devtest.ringcentral.com'

    RINGCENTRAL_USERNAME = '14087081993'
    RINGCENTRAL_PASSWORD = 'Pokemon1029!'
    RINGCENTRAL_EXTENSION = '101'

    rcsdk = SDK( RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
    platform = rcsdk.platform()
    platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)

    platform.post('/restapi/v1.0/account/~/extension/~/sms',
                  {
                      'from' : { 'phoneNumber': RINGCENTRAL_USERNAME },
                      'to'   : [ {'phoneNumber': RECIPIENT} ],
                      'text' : 'Hello World from Python'
                  })

################ END HELPER FUNCTIONS ################
