from django.db import models
from django.utils import timezone
import pickle

# Create your models here.

class Watchlist(models.Model):
    name = models.CharField(max_length=45)

    
class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    nextEarningsDate = models.DateField()
    timestamp = models.DateTimeField()
    
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    
class OptionChain(models.Model):

    #ticker = models.CharField(max_length=5)
    expirationType = models.CharField(max_length=30) # monthly or whatever
    #timestamp =  models.DateTimeField(auto_now_add=True)
    
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    
class Option(models.Model):
    
    CALL = 'CALL'
    PUT = 'PUT'
    
    #ticker = models.CharField(max_length=5)
    optionType = models.CharField(max_length=4)
    #timestamp = models.DateTimeField()
    
     
    nasdaqName = models.CharField(max_length=30)
    contractName = models.CharField(max_length=30)
    last = models.DecimalField(max_digits=8, decimal_places=2)
    change = models.DecimalField(max_digits=4, decimal_places=2)
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    ask = models.DecimalField(max_digits=8, decimal_places=2)
    volume = models.IntegerField()
    openInterest = models.IntegerField()
    strike = models.DecimalField(max_digits=12, decimal_places=2)

    optionChain = models.ForeignKey(OptionChain, on_delete=models.CASCADE)
        
