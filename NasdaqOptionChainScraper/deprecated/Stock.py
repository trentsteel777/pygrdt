from django.db import models
from django.utils import timezone

class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    nextEarningsDate = models.DateField()
    timestamp = models.DateTimeField(
        primary_key=True,
    )
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    
    
