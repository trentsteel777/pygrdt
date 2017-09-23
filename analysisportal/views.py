from django.shortcuts import render
from django.http import JsonResponse
import sys
from .models import *
from datetime import *
from sqlalchemy.sql.expression import false
from decimal import Decimal as D

# Create your views here.

def analyze(request):
    return render(request, 'analysisportal/analyze.html', {})

def grdt(request):
    return render(request, 'analysisportal/index.html', {})

def optionExpiriesList(request):
    qd = getQd(request)
    
    searchWatchlist = qd.__getitem__('watchlist')
    wl = Watchlist.objects.get(name=searchWatchlist)
    wlTickers = wl.ticker_set.all().filter(enabled=True)
    wlTickersSymbolList = wlTickers.values_list('ticker', flat=True)
    
    searchDate = datetime.strptime(qd['searchDate'], "%m/%d/%Y").date()
    searchHour = int(qd['hour'])
    searchDate_from = datetime(searchDate.year, searchDate.month, searchDate.day, searchHour,0,0, tzinfo=timezone.utc)
    searchDate_to = datetime(searchDate.year, searchDate.month, searchDate.day, searchHour + 1, 0, 0, tzinfo=timezone.utc)
  
    expiryList = Option.objects.filter(optionChain__stock__ticker__ticker__in=wlTickersSymbolList, 
                                       optionChain__stock__timestamp__gte=searchDate_from,  
                                       optionChain__stock__timestamp__lt=searchDate_to).values_list('nasdaqName', flat=True).distinct()
                                      
    expiryList = list(filter(None, expiryList)) # Remove any empty strings
    expiryList = sorted(expiryList, key=lambda x: datetime.strptime(x, '%b %d, %Y'))
    
    expiryJsonList = []
    
    for e in expiryList:
        expiryJsonList.append({
                'expiry' : e,
            })
    if expiryJsonList:
        expiryJsonList.insert( 0, {'expiry' : 'ALL'})
        
    
    data = { 'expiryList' : expiryJsonList, 'expiryListTotal' : len(expiryJsonList) }

    return JsonResponse(data)

def strategyJerryLee(request):
    qd = getQd(request)
    
    searchWatchlist = qd.__getitem__('watchlist')
    wl = Watchlist.objects.get(name=searchWatchlist)
    wlTickers = wl.ticker_set.all().filter(enabled=True)
    wlTickersSymbolList = wlTickers.values_list('ticker', flat=True)
    tickersTotal = wlTickers.count()
    
    searchDate = datetime.strptime(qd['searchDate'], "%m/%d/%Y").date()
    searchHour = int(qd['hour'])
    searchDate_from = datetime(searchDate.year, searchDate.month, searchDate.day, searchHour,0,0, tzinfo=timezone.utc)
    searchDate_to = datetime(searchDate.year, searchDate.month, searchDate.day, searchHour + 1, 0, 0, tzinfo=timezone.utc)
    
    start = (int(qd.__getitem__('start')))
    limit = (start + int(qd.__getitem__('limit')))
    
    stocks = Stock.objects.filter(ticker__ticker__in=wlTickersSymbolList, timestamp__gte=searchDate_from, timestamp__lt=searchDate_to)
    
    expiry = qd['expiry']
    
    optionsList = []
    for s in stocks:
        filters = {'optionType': Option.PUT, 'strike__gte': (s.price * D(0.75)), 'strike__lte': (s.price * D(0.85)) }
        if expiry != 'ALL':
            filters['nasdaqName'] = expiry
        optionsList.extend( s.optionchain.option_set.filter(**filters) )
    
    optionsTotal = len(optionsList)
    optionsList = optionsList[start : limit]
    sharesPerContract = 100
    
    optionsJsonArr = []
    for o in optionsList:
        
        stockPrice = o.optionChain.stock.price
        putStrike = o.strike
        
        marginOfSafety = (stockPrice - putStrike) / stockPrice
        returnOnOption = o.bid / ((putStrike * D(0.1)) + o.bid)
        marginPerContract = ((putStrike * D(0.1)) + o.bid) * sharesPerContract
        exposurePerContract = stockPrice * sharesPerContract
        
        optionsJsonArr.append({
            'ticker' : o.optionChain.stock.ticker.ticker,
            'marginOfSafety':marginOfSafety,
            'return': returnOnOption,
            'margin': marginPerContract,
            'exposure': exposurePerContract,
            'earningsDate': o.optionChain.stock.earningsDateStart,

            'putOptionType': o.optionType,
            'putNasdaqName': o.nasdaqName,
            'putContractName': o.contractName,
            'putLast': o.last,
            'putChange': o.change,
            'putBid': o.bid,
            'putAsk': o.ask,
            'putVolume': o.volume,
            'putOpenInterest': o.openInterest,
            'putStrike': putStrike,
            'stockPrice': stockPrice,
            'earningsDate': o.optionChain.stock.earningsDateStart,
            
        })
          
    data = { 'options' : optionsJsonArr, 'optionsTotal' : optionsTotal }

    return JsonResponse(data)
    
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': False,
        'test':[{'hello':45},{'goodbye':55}]
    }
    data = {
           'optionChain' : [{
           'optionType': 'CALL',
           'nasdaqName': 'July, 2017',
           'contractName': '',
           'last': 4.53,
           'change': 0.12,
           'bid': 4.6,
           'ask': 4.7,
           'volume': 1027,
           'openInterest': 504,
           'strike': 125,
       }]
    }
    return JsonResponse(data)

def dispatcher(request):
    qd = getQd(request)
    action = qd.__getitem__('action')
    data = {
         'success': False, 'msg' : 'Server exception'
    }
    if not action:
        return JsonResponse(data)
    try:
        current_module = sys.modules[__name__]
        ajaxMethod = getattr(current_module, action)
        return ajaxMethod(request)
    except:
        return JsonResponse(data)
    
# returns query dictionary from request
def getQd(request):
    if(request.method == "GET"):
        return request.GET
    elif(request.method == "POST"):
        return request.POST
    else:
        return {}

    
def getTickersByWatchlist(request):
    qd = getQd(request)
    searchWatchlist = qd.__getitem__('watchlist')
    watchlist = Watchlist.objects.get(name__exact=searchWatchlist)
    
    tickers = watchlist.ticker_set.all()
    tickersTotal = tickers.count()
    
    tickersJsonArr = []
    for t in tickers:
        tickersJsonArr.append({
            'ticker': t.ticker,
        })
        
    data = { 'tickers' : tickersJsonArr, 'tickersTotal' : tickersTotal }
    return JsonResponse(data)
    
def getWatchlists(request):
    watchlists = Watchlist.objects.filter(enabled=True)
    watchlistsTotal = watchlists.count()
    
    watchlistJsonArr = []
    for watchlist in watchlists:
        watchlistJsonArr.append({
            'name': watchlist.name,
        })
        
    data = { 'watchlists' : watchlistJsonArr, 'watchlistsTotal' : watchlistsTotal }
    return JsonResponse(data)
    
def getOptionChain(request):
    qd = getQd(request)

    start = (int(qd.__getitem__('start'))) * 2
    limit = (start + int(qd.__getitem__('limit'))) * 2
    
    #options = Option.objects.all().order_by('strike')[start:limit]
    #optionTotal = Option.objects.count() / 2
    
    searchTicker = qd['ticker']
    
    searchDate = datetime.strptime(qd['searchDate'], "%m/%d/%Y").date()
    searchHour = int(qd['hour'])
    searchDate_from = datetime(searchDate.year, searchDate.month, searchDate.day, searchHour,0,0, tzinfo=timezone.utc)
    searchDate_to = datetime(searchDate.year, searchDate.month, searchDate.day, searchHour + 1, 0, 0, tzinfo=timezone.utc)
    
    stockList = Stock.objects.filter(ticker__ticker=searchTicker, timestamp__gte=searchDate_from, timestamp__lt=searchDate_to)
    
    stock = None
    if len(stockList) > 0:
        #limit to 1 because the data is 60 times an hour instead of once an hour!
        stock = stockList.get()
        
    options = []
    optionTotal = 0
    optionArr = []
    msg = 'No data for date and time chosen'
    success = False
    
    if stock != None:
        options = stock.optionchain.option_set.all()[start:limit]
        optionTotal = stock.optionchain.option_set.count() / 2
        
        if len(options) > 0:
            msg = 'Data found for date and time'
            success = True
        
        
        for i in range(0, len(options),2):
            if options[i].optionType == 'CALL':
                call = options[i]
                put = options[i+1]
            elif options[i].optionType == 'PUT':
                call = options[i+1]
                put = options[i]
            optionArr.append({
                'callOptionType': call.optionType,
                'callNasdaqName': call.nasdaqName,
                'callContractName': call.contractName,
                'callLast': call.last,
                'callChange': call.change,
                'callBid': call.bid,
                'callAsk': call.ask,
                'callVolume': call.volume,
                'callOpenInterest': call.openInterest,
                'callStrike': call.strike,
                
                'putOptionType': put.optionType,
                'putNasdaqName': put.nasdaqName,
                'putContractName': put.contractName,
                'putLast': put.last,
                'putChange': put.change,
                'putBid': put.bid,
                'putAsk': put.ask,
                'putVolume': put.volume,
                'putOpenInterest': put.openInterest,
                'putStrike': put.strike,
            })
    data = { 'optionChain' : optionArr, 'optionTotal' : optionTotal, 'success': success, 'msg' : msg }
    return JsonResponse(data)