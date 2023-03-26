import json
import uuid

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from celery_dynamic_schedule.models import CeleryDynamicSchedule
from strategy.models import TradingViewStrategy
from strategy.tasks.third_party import third_party_manager


@receiver(post_save, sender=TradingViewStrategy)
def create_periodic_task(sender, instance: TradingViewStrategy, **kwargs):
    CeleryDynamicSchedule.objects.update_or_create(
        task=settings.TRADINGVIEW_STRATEGY_CHECK_TASK,
        task_args=json.dumps([instance.id, ]),
        defaults={
            "name": f'{instance.name}-{uuid.uuid4()}',
            'crontab_code': instance.crontab_code,

        }
    )
    if instance.broker_is_active:
        third_party_manager.apply_async(
            args=(
                {
                    "message": "strategy was changed and broker is active",
                    "broker": instance.get_broker_display()
                },
                settings.TELEGRAM_MODULE
            ),
            kwargs={'chat_id': instance.telegram_id}
        )
