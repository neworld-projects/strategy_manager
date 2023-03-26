import datetime
import logging

from celery import shared_task
from django.conf import settings

from services.tradingview.simple.websocket import WebSocketConnectionChartForStrategyManager
from strategy.models import TradingViewStrategy


@shared_task(
    name=settings.TRADINGVIEW_STRATEGY_CHECK_TASK,
    time_limit=datetime.timedelta(minutes=settings.SHARED_TASK_TIME_LIMIT).seconds
)
def check_tradingview_strategy(instance_id):
    logging.info(f"tobe start instance: {instance_id}")
    try:
        instance = TradingViewStrategy.objects.get(id=instance_id, is_active=True)
        WebSocketConnectionChartForStrategyManager(instance)
    except TradingViewStrategy.DoesNotExist:
        logging.error('DoesNotExist')

