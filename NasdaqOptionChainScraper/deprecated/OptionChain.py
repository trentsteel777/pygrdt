import pickle

class OptionChain:
    callList = []
    putList = []

    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
    expirationType = models.CharField(max_length=30) # monthly or watever
    timestamp =  models.DateTimeField(auto_now_add=True)
    
    stock = models.ForeignKey(OptionChain, on_delete=models.CASCADE)

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

    
    
