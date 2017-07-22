from analysisportal.util.web import getWebsitHtmlAsBs4
from datetime import datetime, timedelta, time, date
from analysisportal.models import ExchangeHoliday
import re

# Add 15 minutes to give scraper a chance to get EOD price data
nasdaqClosingTime = time(hour=21, minute=15) # assumes UTC

# returns None if exchange is closed
def timeNasdaqIsOpenTo():
    sat = 5
    sun = 6
    currentDay = date.today().weekday()
    
    # Nasdaq won't be open on the weekend
    if currentDay == sat and currentDay == sun:
        return None
    
    try:
        holiday = ExchangeHoliday.objects.get(date=date.today())
    except ExchangeHoliday.DoesNotExist:
        return nasdaqClosingTime

    # This will be null if exchange is closed all day
    return holiday.openToTime 
    
    

def scrapeAndSaveNasdaqHolidays():
    url ='http://www.nasdaqtrader.com/Trader.aspx?id=Calendar'

    parsedHtml = getWebsitHtmlAsBs4(url)

    holidayTables = parsedHtml.body.find_all('div', class_='dataTable')

    thisYear = datetime.now().year
    thisYearTable = None
    for table in holidayTables:
        tableYear = int( table.find_all(text=re.compile('^\d+$'))[0] )
        if thisYear == tableYear:
            thisYearTable = table
            break
        
    trs = thisYearTable.find_all('tr')[1:] # Remove header
    
    for tr in trs:
        tds = tr.find_all('td')
        
        holidayDate = datetime.strptime(tds[0].text, '%B %d, %Y').date()
        holidayDescription = tds[1].text
        openTillTimeUtc = None
        
        if tds[2].text != 'Closed':
            removePeriods = tds[2].text.replace('.', '')
            openTillTimeEst = datetime.strptime(removePeriods, '%I:%M %p')
            openTillTimeUtc = ( openTillTimeEst + timedelta(hours=5) ).time()
        
        exHol = ExchangeHoliday()
        exHol.date = holidayDate
        exHol.description = holidayDescription
        exHol.openToTime = openTillTimeUtc
        exHol.save()
    
