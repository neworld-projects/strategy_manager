from django.db import models


# Create your models here.
class TradingViewStrategy(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    settings = models.TextField(max_length=10000)
    is_active = models.BooleanField(default=True)
