import json

from django.conf import settings
from django.db import models
# Create your models here.
from django.utils import timezone
from django_celery_beat.models import PeriodicTask

from strategy.enums import TimeInterval


class TradingViewStrategy(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    running_interval = models.CharField(choices=TimeInterval.choices, max_length=15)
    settings = models.TextField(max_length=10000)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(TradingViewStrategy, self).save(**kwargs)

        PeriodicTask.objects.create(
            name=self.name,
            task=settings.TRADINGVIEW_STRATEGY_CHECK_TASK,
            interval_id=TimeInterval.convert_to_interval_model(self.running_interval),
            args=json.dumps([self.id]),
            start_time=timezone.now().replace(
                hour=TimeInterval.get_hour(self.running_interval),
                minute=TimeInterval.get_minute(self.running_interval),
                second=0,
                microsecond=0
            )
        )
