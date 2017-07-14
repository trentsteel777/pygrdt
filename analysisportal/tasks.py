from datetime import datetime

from analysisportal.pricescrapers.nasdaqScraper import  scraper
from analysisportal.exchangeopenhours.nasdaqhours import timeNasdaqIsOpenTo
from analysisportal.models import Ticker, Watchlist

@task
def scrapeNasdaqWebsite():
    pass
    
    closingTime = timeNasdaqIsOpenTo()
    if (closingTime == None) or (datetime.now().time() >= closingTime):
        return
    
    enabledTickers = Ticker.objects.order_by().filter(watchlist__enabled__exact=True).distinct()
    for ticker in enabledTickers:
        scraper(ticker)
    

