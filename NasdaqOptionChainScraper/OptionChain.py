import pickle

class OptionChain:
    callList = []
    putList = []

    ticker = ''
    expirationType = '' # monthly or watever
    timeCreated = None

    def __init__(self, ticker, expirationType, timeCreated):
        self.ticker = ticker
        self.expirationType = expirationType
        self.timeCreated = timeCreated

    def saveToPickle(self):
        fileName = self.toFileName()
        with open(fileName, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print ('Saved file: ' + fileName)
        
    def toFileName(self):
        return self.ticker + '_' + self.expirationType + '_' + str(self.timeCreated) + '.pkl'

    
    
