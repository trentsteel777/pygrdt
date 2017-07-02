import urllib.request
import time
from bs4 import BeautifulSoup
from models import OptionChain
from OptionExtracter import extractOptions

def getWebsitHtmlAsBs4(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    nasdaqHtml = mybytes.decode("utf8")
    fp.close()

    return BeautifulSoup(nasdaqHtml, 'lxml')


parsedHtml = getWebsitHtmlAsBs4("http://www.nasdaq.com/symbol/aapl/option-chain?money=all&expir=stan&page=1")
forms = [ parsedHtml.body.find(id="optionchain") ]

subsequentPages = []
pager = parsedHtml.find(id='pager').find_all('a')
for a in pager:
    if a.text.isnumeric():
        subsequentPages.append( a['href'] )

for url in subsequentPages:
    parsedHtml = getWebsitHtmlAsBs4(url)
    forms.append( parsedHtml.body.find(id="optionchain") )

optionChain = OptionChain('AAPL', 'MONTHLY', time.time())
for form in forms:
    trList = form.find('table').find_all('tr')[1:] # Remove header
    extractOptions(optionChain, trList)

optionChain.saveToPickle()
    

