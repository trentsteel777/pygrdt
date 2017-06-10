import pickle

class OptionChain:
    callList = []
    putList = []

    ticker = ''
    expirationType = '' # monthly or watever
    timestamp = None

    def __init__(self, ticker, expirationType, timestamp):
        self.ticker = ticker
        self.expirationType = expirationType
        self.timestamp = timestamp

    def saveToPickle(self):
        fileName = self.toFileName()
        with open(fileName, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print ('Saved file: ' + fileName)
        
    def toFileName(self):
        return self.ticker + '_' + self.expirationType + '_' + str(self.timestamp) + '.pkl'

    
    
