
import time
from analysisportal.util.web import getWebsitHtmlAsBs4
from analysisportal.models import Watchlist, Ticker, Stock, OptionChain, Option
from datetime import datetime
from django.utils import timezone
from celery.bin.call import call
import pickle
import os, sys

DEBUG_MODE = True

def getEarningsDateFromYahoo(symbol):
    yahooParsedHtml = getWebsitHtmlAsBs4("https://finance.yahoo.com/quote/" + symbol +"/")
    earningsDateLiteral = yahooParsedHtml.body.find(attrs={"data-test" : "EARNINGS_DATE-value"}).text
    earningsDate =  datetime.strptime(earningsDateLiteral, '%b %d, %Y').date()
    return earningsDate
    
    
# Takes an analysisportal.models.Ticker instance
def scraper(ticker):
    symbol = ticker.ticker
    earningsDate = getEarningsDateFromYahoo(symbol)
    
    parsedHtml = getWebsitHtmlAsBs4("http://www.nasdaq.com/symbol/" + symbol + "/option-chain?money=all&expir=stan&page=1")
    stockPrice = ( parsedHtml.body.find(id="qwidget_lastsale").text[1:] ) # Remove dollar sign
    
    forms = [ parsedHtml.body.find(id="optionchain") ]
    
    subsequentPages = []
    pager = parsedHtml.find(id='pager').find_all('a')
    for a in pager:
        if a.text.isnumeric():
            subsequentPages.append( a['href'] )
    
    for url in subsequentPages:
        parsedHtml = getWebsitHtmlAsBs4(url)
        forms.append( parsedHtml.body.find(id="optionchain") )
    
    
    stock = Stock()
    stock.price = stockPrice
    stock.timestamp = timezone.now()
    stock.nextEarningsDate = earningsDate
    
    
    optionChain = OptionChain()
    optionChain.expirationType = 'MONTHLY'
    
    
    extractedOptions = {'calls': [], 'puts': []}
    for form in forms:
        trList = form.find('table').find_all('tr')[1:] # Remove header
        call, put = extractOptions(trList)
        extractedOptions['calls'].append(call)
        extractedOptions['puts'].append(put)
    
    if not DEBUG_MODE:
        persistPrices(ticker, stock, optionChain, extractedOptions)
    else:
        savePricesToPickle(ticker, stock, optionChain, extractedOptions)
        
    
def persistPrices(ticker, stock, optionChain, callsAndPutsMap):
    stock.ticker = ticker
    stock.save()
    
    optionChain.stock = stock
    optionChain.save()
    
    for key in callsAndPutsMap.keys():
        for option in callsAndPutsMap[key]:
            option.optionChain = optionChain
            option.save()
    
    
def savePricesToPickle(ticker, stock, optionChain, extractedOptions):
    
    optionData = {
        'ticker' : ticker,
        'stock' : stock,
        'optionChain' : optionChain,
        'extractedOptions' : extractedOptions
        
    }
    PICKLE_DIR = os.path.join(os.getcwd(), 'analysisportal/pricescrapers/data/nasdaq')
    fileName = os.path.join(PICKLE_DIR, ticker.ticker + '_' + time.strftime("%Y_%m_%d_%H_%M") +'.pickle')
    with open(fileName, 'wb') as handle:
        pickle.dump(optionData, handle, protocol=pickle.HIGHEST_PROTOCOL)
        

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




def extractOptions(trList):
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
        
        return call, put
        
# could be better validation around these helper methods
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
