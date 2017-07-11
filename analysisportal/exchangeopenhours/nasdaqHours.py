from analysisportal.util.web import getWebsitHtmlAsBs4
from datetime import datetime, timedelta
from analysisportal.models import ExchangeHoliday
import re

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
    
