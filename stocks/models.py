from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StockList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stocklist", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Stock(models.Model):
    connctedlist = models.ForeignKey(StockList, on_delete=models.CASCADE)
    company = models.CharField(max_length=300)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=7,decimal_places=2)

    def __str__(self):
        return "Stock: " + self.symbol + " Price: " + str(self.price)
