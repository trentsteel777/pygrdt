from models import Option

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


def extractOptions(optionChain, trList):
    for tr in trList:
        tdList = tr.find_all('td')
        call = Option()
        call.optionType = 'CALL'
        call.nasdaqName   = tdList[callNameIndex]        .text
        call.last         = tdList[callLastIndex]        .text
        call.change       = tdList[callChangeIndex]      .text
        call.bid          = tdList[callBidIndex]         .text
        call.ask          = tdList[callAskIndex]         .text
        call.volume       = tdList[callVolumeIndex]      .text
        call.openInterest = tdList[callOpenInterestIndex].text
        call.ticker       = tdList[tickerIndex]          .text
        call.strike       = tdList[strikeIndex]          .text
        call.optionChain.add(optionChain)
        
        put = Option()
        put.optionType = 'PUT'
        put.nasdaqName   = tdList[putNameIndex]        .text
        put.last         = tdList[putLastIndex]        .text
        put.change       = tdList[putChangeIndex]      .text
        put.bid          = tdList[putBidIndex]         .text
        put.ask          = tdList[putAskIndex]         .text
        put.volume       = tdList[putVolumeIndex]      .text
        put.openInterest = tdList[putOpenInterestIndex].text
        put.ticker       = tdList[tickerIndex]         .text
        put.strike       = tdList[strikeIndex]         .text
        put.optionChain.add(optionChain)
