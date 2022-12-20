from django.db import models

from strategy.enums import TimeInterval, TimeframeChoice


class TradingViewStrategy(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    running_interval = models.CharField(choices=TimeInterval.choices, max_length=15, db_index=True)
    settings = models.JSONField()
    symbol = models.CharField(max_length=20)
    timeframe = models.IntegerField(choices=TimeframeChoice.choices, db_index=True)
    is_active = models.BooleanField(default=False, db_index=True)
    base_capital = models.IntegerField(default=100)
