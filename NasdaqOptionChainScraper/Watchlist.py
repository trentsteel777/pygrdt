from django.db import models
from django.utils import timezone

class Watchlist(models.Model):
    title = models.CharField(max_length=200)
    tickers = []


    def __str__(self):
        return self.title
