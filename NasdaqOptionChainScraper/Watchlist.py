from django.db import models
from django.utils import timezone

class Watchlist(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name
