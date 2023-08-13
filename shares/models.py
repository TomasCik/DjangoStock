from django.db import models

# Create your models here.


class Stock(models.Model):
    ticker = models.CharField(max_length=10, null=True, blank=True )
    companyName = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.ticker





