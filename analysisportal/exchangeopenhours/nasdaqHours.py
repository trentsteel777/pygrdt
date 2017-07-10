from util.web import getWebsitHtmlAsBs4
from datetime import datetime

def isOpen():
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
        date = tds[0]
        description = tds[1]
        openTill = tds[2]
        
    
def scrapeAndSaveExchangeHolidaysFromNasdaqWebsite():
    