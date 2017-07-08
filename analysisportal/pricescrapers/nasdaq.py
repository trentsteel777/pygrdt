import urllib.request
import time
from bs4 import BeautifulSoup
from analysisportal.models import Watchlist, Ticker, Stock, OptionChain
from analysisportal.models import Option
from datetime import datetime

def getWebsitHtmlAsBs4(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    nasdaqHtml = mybytes.decode("utf8")
    fp.close()

    return BeautifulSoup(nasdaqHtml, 'lxml')


def scraper():
    parsedHtml = getWebsitHtmlAsBs4("http://www.nasdaq.com/symbol/aapl/option-chain?money=all&expir=stan&page=1")
    forms = [ parsedHtml.body.find(id="optionchain") ]
    
    subsequentPages = []
    pager = parsedHtml.find(id='pager').find_all('a')
    for a in pager:
        if a.text.isnumeric():
            subsequentPages.append( a['href'] )
    
    for url in subsequentPages:
        parsedHtml = getWebsitHtmlAsBs4(url)
        forms.append( parsedHtml.body.find(id="optionchain") )
    
    
    ticker = Ticker.objects.get(ticker='AAPL')
    
    stock = Stock()
    stock.price = 142.27
    stock.timestamp = datetime.now()
    
    #ticker.stock_set.add(stock)
    stock.ticker = ticker
    stock.save()
    
    optionChain = OptionChain()
    optionChain.expirationType = 'MONTHLY'
    optionChain.stock = stock
    optionChain.save()
    
    for form in forms:
        trList = form.find('table').find_all('tr')[1:] # Remove header
        extractOptions(optionChain, trList)
    
    #ptionChain.stock_set.add(stock)
    


callNameIndex = 0
callLastIndex = 1
callChangeIndex = 2
callBidIndex = 3
callAskIndex = 4
callVolumeIndex = 5
callOpenInterestIndex = 6

tickerIndex = 7
strikeIndex = 8

putNameIndex = 9
putLastIndex = 10
putChangeIndex = 11
putBidIndex = 12
putAskIndex = 13
putVolumeIndex = 14
putOpenInterestIndex = 15

def toFloat(value):
  try:
    f = float(value)
    return f
  except ValueError:
    return 0.0

def toInt(value):
  try:
    i = int(value)
    return i
  except ValueError:
    return 0


def extractOptions(optionChain, trList):
    for tr in trList:
        tdList = tr.find_all('td')
        call = Option()
        call.optionType = 'CALL'
        call.nasdaqName   = tdList[callNameIndex]               .text
        call.last         = toFloat( tdList[callLastIndex]      .text )
        call.change       = toFloat( tdList[callChangeIndex]    .text )
        call.bid          = toFloat( tdList[callBidIndex]       .text )
        call.ask          = toFloat( tdList[callAskIndex]       .text )
        call.volume       = toInt( tdList[callVolumeIndex]      .text )
        call.openInterest = toInt( tdList[callOpenInterestIndex].text )
        call.strike       = toFloat( tdList[strikeIndex]        .text )
        
        call.optionChain = optionChain
        call.save()
        #optionChain.option_set.add(call)
        
        put = Option()
        put.optionType = 'PUT'
        put.nasdaqName   = tdList[putNameIndex]               .text
        put.last         = toFloat( tdList[putLastIndex]      .text )
        put.change       = toFloat( tdList[putChangeIndex]    .text )
        put.bid          = toFloat( tdList[putBidIndex]       .text )
        put.ask          = toFloat( tdList[putAskIndex]       .text )
        put.volume       = toInt( tdList[putVolumeIndex]      .text )
        put.openInterest = toInt( tdList[putOpenInterestIndex].text )
        put.strike       = toFloat( tdList[strikeIndex]       .text )
        
        put.optionChain = optionChain
        put.save()
        #optionChain.option_set.add(put)
