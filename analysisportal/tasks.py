from __future__ import absolute_import, unicode_literals
from celery import shared_task


    
@shared_task
def scrapeNasdaqWebsite():
    import time
    from datetime import datetime
    from analysisportal.models import Ticker, Watchlist
    from analysisportal.pricescrapers.nasdaqScraper import  scraper
    from analysisportal.exchangeopenhours.nasdaqHours import timeNasdaqIsOpenTo
    
    closingTime = timeNasdaqIsOpenTo()
    currentTime = datetime.now().time()
    if (closingTime == None) or ( (currentTime >= closingTime) and (currentTime.hour >= 15) ):
        return 'Nasdaq is closed . No options scraped.'
    
    enabledTickers = Ticker.objects.order_by().filter(watchlist__enabled__exact=True).distinct()
    for ticker in enabledTickers:
        scraper(ticker)
        
    symbolList = [t.ticker for t in enabledTickers]
    return 'scraped option data for ' + str(symbolList)
        
@shared_task
def add(x, y):
    return x + y


