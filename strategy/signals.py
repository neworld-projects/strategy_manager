import json

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import PeriodicTask

from strategy.enums import TimeInterval
from strategy.models import TradingViewStrategy


@receiver(post_save, sender=TradingViewStrategy)
def create_periodic_task(sender, instance, **kwargs):
    PeriodicTask.objects.get_or_create(
        name=instance.name,
        defaults={
            "name": instance.name,
            "task": settings.TRADINGVIEW_STRATEGY_CHECK_TASK,
            "interval": TimeInterval.convert_to_interval_model(instance.running_interval)[0],
            "args": json.dumps([instance.id, ]),
            "start_time": timezone.now().replace(**TimeInterval.get_replace_args(instance.running_interval))
        }
    )
