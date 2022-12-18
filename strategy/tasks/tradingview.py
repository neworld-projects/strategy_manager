from celery import shared_task
from django.conf import settings


@shared_task(name=settings.TRADINGVIEW_STRATEGY_CHECK_TASK)
def check_tradingview_strategy(instance_id: int):
    pass
