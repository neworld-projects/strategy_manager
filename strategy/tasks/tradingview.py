from celery import shared_task
from django.conf import settings

from strategy.models import TradingViewStrategy
from utils.tradingview.simple.websocket import WebSocketConnectionSampleChart


@shared_task(name=settings.TRADINGVIEW_STRATEGY_CHECK_TASK)
def check_tradingview_strategy(instance_id: int):
    instance = TradingViewStrategy.objects.get(id=instance_id)
    WebSocketConnectionSampleChart(instance.symbol, instance.timeframe, instance.settings)