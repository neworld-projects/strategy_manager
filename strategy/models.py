import json

from django.conf import settings
from django.db import models
# Create your models here.
from django.utils import timezone
from django_celery_beat.models import PeriodicTask

from strategy.enums import TimeInterval, TimeframeChoice


class TradingViewStrategy(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    running_interval = models.CharField(choices=TimeInterval.choices, max_length=15, db_index=True)
    settings = models.TextField(max_length=10000)
    symbol = models.CharField(max_length=20)
    timeframe = models.IntegerField(choices=TimeframeChoice.choices, db_index=True)
    is_active = models.BooleanField(default=False, db_index=True)

    def save(self, *args, **kwargs):
        super(TradingViewStrategy, self).save(**kwargs)

        PeriodicTask.objects.create(
            name=self.name,
            task=settings.TRADINGVIEW_STRATEGY_CHECK_TASK,
            interval_id=TimeInterval.convert_to_interval_model(self.running_interval),
            args=json.dumps([self.id]),
            start_time=timezone.now().replace(
                minute=TimeInterval.get_minute(self.running_interval),
                hour=TimeInterval.get_hour(self.running_interval),
                second=TimeInterval.get_second(self.running_interval),
                microsecond=0
            )
        )
