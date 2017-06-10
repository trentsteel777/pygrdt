class Option:
    type = None
    nasdaqName = ''
    contractName = 'UNKNOWN'
    last = 0
    change = 0
    bid = 0
    ask = 0
    volume = 0
    openInterest = 0
    ticker = ''
    strike = 0

    def getIds(self):
        return '[ ' + self.ticker + ' ' + self.type + ' ' + self.nasdaqName + ' ]'
