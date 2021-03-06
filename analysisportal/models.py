from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils import timezone
import pickle

# Create your models here.

class ExchangeHoliday(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=45)
    openToTime = models.TimeField(null=True) # null if closed all day # UTC
    
    
class Watchlist(models.Model):
    name = models.CharField(max_length=45, unique=True)
    enabled = models.BooleanField(default=False)
    
class Ticker(models.Model):
    ticker = models.CharField(max_length=5, unique=True)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    
class Stock(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2)
    earningsDateStart = models.DateField(null=True)
    earningsDateEnd = models.DateField(null=True,default=None)
    timestamp = models.DateTimeField()
    
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    
class OptionChain(models.Model):

    expirationType = models.CharField(max_length=30) # monthly or whatever
    stock = models.OneToOneField(
        Stock,
        on_delete=models.CASCADE,
    )
    
    def saveToPickle(self):
        fileName = self.toFileName()
        with open(fileName, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print ('Saved file: ' + fileName)
        
    def toFileName(self):
        return self.stock.ticker + '_' + self.expirationType + '_' + str(self.stock.timestamp) + '.pkl'
    
class Option(models.Model):
    
    CALL = 'CALL'
    PUT = 'PUT'
    
    optionType   = models.CharField(max_length=4)
    expiry       = models.DateField(null=True)
    contractName = models.CharField(max_length=30, null=True)
    last         = models.DecimalField(max_digits=8, decimal_places=2)
    change       = models.DecimalField(max_digits=4, decimal_places=2)
    bid          = models.DecimalField(max_digits=8, decimal_places=2)
    ask          = models.DecimalField(max_digits=8, decimal_places=2)
    volume       = models.IntegerField()
    openInterest = models.IntegerField()
    strike       = models.DecimalField(max_digits=12, decimal_places=2)

    optionChain = models.ForeignKey(OptionChain, on_delete=models.CASCADE)
        
