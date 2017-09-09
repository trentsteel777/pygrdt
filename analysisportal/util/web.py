import urllib.request
from bs4 import BeautifulSoup

import logging

logger = logging.getLogger(__name__)

def getWebsiteHtmlAsBs4(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    
    try:
        html = mybytes.decode() # previously pass 'utf-8' as a parameter
    except UnicodeDecodeError as err:
        logger.warning('getWebsiteHtmlAsBs4(' + url + ')' + str(err))
        return None
        
    fp.close()

    return BeautifulSoup(html, 'lxml')