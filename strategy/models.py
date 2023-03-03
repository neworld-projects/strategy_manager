from django.db import models

from strategy.enums import TimeframeChoice, TradingViewScriptModeChoice, ChartTypeChoice, Broker


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
    telegram_id = models.CharField(max_length=20)
    broker_is_active = models.BooleanField(default=False)
    broker = models.IntegerField(choices=Broker.choices, default=Broker.BINANCE, db_index=True)
    chart_type = models.IntegerField(choices=ChartTypeChoice.choices, db_index=True, default=ChartTypeChoice.SAMPLE)
