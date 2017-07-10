import urllib.request
from bs4 import BeautifulSoup


def getWebsitHtmlAsBs4(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    html = mybytes.decode("utf8")
    fp.close()

    return BeautifulSoup(html, 'lxml')