import datetime

from celery import shared_task
from django.conf import settings

from services.tradingview.simple.websocket import WebSocketConnectionSampleChart
from strategy.models import TradingViewStrategy


@shared_task(
    name=settings.TRADINGVIEW_STRATEGY_CHECK_TASK,
    time_limit=datetime.timedelta(minutes=settings.SHARED_TASK_TIME_LIMIT)
)
def check_tradingview_strategy(instance_id: int):
    instance = TradingViewStrategy.objects.get(id=instance_id, is_active=True)
    WebSocketConnectionSampleChart(instance)
