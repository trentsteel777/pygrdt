from __future__ import absolute_import, unicode_literals
from celery import shared_task


    
@shared_task
def scrapeNasdaqWebsite():
    import time
    from datetime import date, datetime, time, timedelta
    from analysisportal.models import Ticker, Watchlist
    from analysisportal.pricescrapers.nasdaqScraper import  scraper
    from analysisportal.exchangeopenhours.nasdaqHours import timeNasdaqIsOpenTo
    
    # Add 30 minutes to get end of day data
    closingTime = (datetime.combine(date.today(), timeNasdaqIsOpenTo()) + timedelta(minutes=30)).time()
    currentTime = datetime.now().time()
    if (closingTime == None) or ( (currentTime >= closingTime) and (currentTime.hour >= 15) ):
        return 'Nasdaq is closed . No options scraped.'
    
    enabledTickers = Ticker.objects.order_by().filter(watchlist__enabled__exact=True).distinct()
    for ticker in enabledTickers:
        try:
            scraper(ticker)
        except:
            pass
        
        
    symbolList = [t.ticker for t in enabledTickers]
    return 'scraped option data for ' + str(symbolList)
        
@shared_task
def add(x, y):
    import pickle
    import time
    import os
    sum = x + y
    PICKLE_DIR = os.path.join(os.getcwd(), 'analysisportal/pricescrapers/data/nasdaq')
    fileName = os.path.join(PICKLE_DIR, 'ADD_' + time.strftime("%Y_%m_%d_%H_%M") +'.pickle')
    with open(fileName, 'wb') as handle:
        pickle.dump(sum, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return x + y


