
import time
from analysisportal.util.web import getWebsiteHtmlAsBs4
from analysisportal.models import Watchlist, Ticker, Stock, OptionChain, Option
from datetime import datetime
from django.utils import timezone
from celery.bin.call import call
import pickle
import os, sys
import logging
from celery.utils import objects

DEBUG_MODE = False
logger = logging.getLogger(__name__)

    
def getEarningsDateFromYahoo(symbol):
    earningsDateStart = None
    earningsDateEnd = None
        
    try:
        yahooParsedHtml = getWebsiteHtmlAsBs4("https://finance.yahoo.com/quote/" + symbol +"/")
        earningsDateLiteral = yahooParsedHtml.body.find(attrs={"data-test" : "EARNINGS_DATE-value"}).text
    except Exception as err:
        logger.warn('getEarningsDateFromYahoo( ' + symbol.upper() + ' ): ' + str(err))
        return (earningsDateStart, earningsDateEnd)
    
    if 'N/A' in earningsDateLiteral:
        return (earningsDateStart, earningsDateEnd)
    elif '-' not in earningsDateLiteral:
        earningsDateStart =  datetime.strptime(earningsDateLiteral.strip(), '%b %d, %Y').date()
        earningsDateEnd = None
    elif '-' in earningsDateLiteral:
        dates = earningsDateLiteral.split('-')
        startLiteral = dates[0].strip()
        endLiteral = dates[1].strip()
        earningsDateStart =  datetime.strptime(startLiteral, '%b %d, %Y').date()
        earningsDateEnd = datetime.strptime(endLiteral, '%b %d, %Y').date()
        
    return (earningsDateStart, earningsDateEnd)
    
    
# Takes an analysisportal.models.Ticker instance
def scraper(ticker):
    symbol = ticker.ticker
    earningsDateStart, earningsDateEnd  = getEarningsDateFromYahoo(symbol)
    
    url = "http://www.nasdaq.com/symbol/" + symbol + "/option-chain?money=all&expir=stan&page=1"
    errMsg = 'Failed to scrape option prices for ' + url
    
    genMsg = 'scraping for: ' + url
    logger.info(genMsg)
    
    parsedHtml = getWebsiteHtmlAsBs4(url)
    if parsedHtml is None:
        logger.error(errMsg)
        return symbol + ' -> Could not reach url or decode it.'
    
    try:
        stockPrice = parsedHtml.body.find(id="qwidget_lastsale").text[1:] # Remove dollar sign
    except AttributeError as aErr:
        logger.error('scraper( ' + symbol.upper() + ' ). Could not get price. May be an invalid symbol. Error message: ' + str(aErr))
        return symbol + ' -> Could not get price. May be an invalid symbol.'
        
    subsequentPages = []
    pager = parsedHtml.find(id='pager').find_all('a')
    for a in pager:
        if a.text.isnumeric():
            subsequentPages.append( a['href'] )
    
    forms = [ parsedHtml.body.find(id="optionchain") ]
    for url in subsequentPages:
        logger.info(genMsg)
        parsedHtml = getWebsiteHtmlAsBs4(url)
        if parsedHtml is not None:
            forms.append( parsedHtml.body.find(id="optionchain") )
        elif parsedHtml is None:
            logger.error(errMsg)
    
    
    stock = Stock()
    stock.price = stockPrice
    stock.timestamp = timezone.now()
    stock.earningsDateStart = earningsDateStart
    stock.earningsDateEnd = earningsDateEnd
    
    optionChain = OptionChain()
    optionChain.expirationType = 'MONTHLY'
    
    
    extractedOptions = {'calls': [], 'puts': []}
    for form in forms:
        trList = form.find('table').find_all('tr')[1:] # Remove header
        calls, puts = extractOptions(trList)
        extractedOptions['calls'].extend(calls)
        extractedOptions['puts'].extend(puts)
    
    if not DEBUG_MODE:
        persistPrices(ticker, stock, optionChain, extractedOptions)
    else:
        savePricesToPickle(ticker, stock, optionChain, extractedOptions)
        
    return 'Successfully scraped ' + symbol
        
    
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
        
def readSavedPricesFromPickle(fileName):
    objects = []
    with (open(fileName, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects

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
    calls = []
    puts = []
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
        
        calls.append(call)
        puts.append(put)
        
    return calls, puts
        
# could be better validation around these helper methods
def toFloat(value):
  try:
    f = float(value)
    return f
  except ValueError as vErr:
    #logger.info(str(vErr))
    return 0.0

def toInt(value):
  try:
    i = int(value)
    return i
  except ValueError as vErr:
    #logger.info(str(vErr))
    return 0
