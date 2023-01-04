import json
import uuid

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from celery_dynamic_schedule.models import CeleryDynamicSchedule
from strategy.models import TradingViewStrategy


@receiver(post_save, sender=TradingViewStrategy)
def create_periodic_task(sender, instance: TradingViewStrategy, **kwargs):
    CeleryDynamicSchedule.objects.get_or_create(
        name=f'{instance.name}-{uuid.uuid4()}',
        defaults={
            "name": f'{instance.name}-{uuid.uuid4()}',
            "task": settings.TRADINGVIEW_STRATEGY_CHECK_TASK,
            "task_kwargs": json.dumps([instance.id, ]),
            'crontab_code': instance.crontab_code
        }
    )
