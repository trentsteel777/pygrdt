from django.db import models
from django.utils import timezone

class Watchlist(models.Model):
    name = models.CharField(max_length=200)
    tickers = models.ForeignKey(Reporter, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
