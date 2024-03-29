from django.db import models

from strategy.enums import TimeframeChoice, TradingViewScriptModeChoice, Broker, MarginType
from strategy.help_texts import strategy_model_help_text


class TradingViewStrategy(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    crontab_code = models.CharField(max_length=50, db_index=True)
    symbol = models.CharField(max_length=20)
    timeframe = models.IntegerField(choices=TimeframeChoice.choices, db_index=True)
    is_active = models.BooleanField(default=False, db_index=True)
    base_capital = models.IntegerField(default=100)
    pine_id = models.CharField(max_length=64)
    pine_version = models.CharField(max_length=7)
    script_mode = models.CharField(
        choices=TradingViewScriptModeChoice.choices,
        default=TradingViewScriptModeChoice.INDICATOR,
        max_length=20
    )
    strategy_model = models.JSONField(default=dict, help_text=strategy_model_help_text)
    telegram_id = models.CharField(max_length=20)
    broker_is_active = models.BooleanField(default=False)
    broker = models.IntegerField(choices=Broker.choices, default=Broker.BINANCE, db_index=True)
    leverage = models.IntegerField(default=1)
    margin_type = models.IntegerField(choices=MarginType.choices, default=MarginType.ISOLATED, db_index=True)
