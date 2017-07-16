from __future__ import absolute_import, unicode_literals
from celery import shared_task


    
@shared_task
def scrapeNasdaqWebsite():
    import time
    from datetime import datetime
    return Ticker.objects.all()[0].ticker
    #from analysisportal.models import Ticker, Watchlist
    #from analysisportal.pricescrapers.nasdaqScraper import  scraper
    #from analysisportal.exchangeopenhours.nasdaqhours import timeNasdaqIsOpenTo
    
    closingTime = timeNasdaqIsOpenTo()
    if (closingTime == None) or (datetime.now().time() >= closingTime):
        return
    
    enabledTickers = Ticker.objects.order_by().filter(watchlist__enabled__exact=True).distinct()
    for ticker in enabledTickers:
        scraper(ticker)
        
@shared_task
def add(x, y):
    return x + y


