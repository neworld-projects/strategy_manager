from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeframeChoice(models.IntegerChoices):
    FIVE_MINUTES = 0, '{"name": "5", "timestamp": 300}'
    FIFTEEN_MINUTES = 1, '{"name": "15", "timestamp": 4500}'
    THIRTY_MINUTES = 2, '{"name": "30", "timestamp": 1800}'
    SIXTY_MINUTES = 3, '{"name": "60", "timestamp": 3600}'
    TOW_HOURS = 4, '{"name": "120", "timestamp": 7200}'
    THREE_HOURS = 5, '{"name": "180", "timestamp": 10800}'
    FOUR_HOURS = 6, '{"name": "240", "timestamp": 14400}'
    ONE_DAY = 7, '{"name": "1D", "timestamp": 86400}'
    ONE_WEEK = 8, '{"name": "1W", "timestamp": 604800}'


class TradingViewScriptModeChoice(models.TextChoices):
    STRATEGY = 'strategy', _('strategy')
    INDICATOR = 'indicator', _('indicator')


class Broker(models.IntegerChoices):
    BINANCE = 0, 'binance'


class MarginType(models.IntegerChoices):
    ISOLATED = 0, 'ISOLATED'
    CROSSED = 1, 'CROSSED'


class PositionKeys(models.TextChoices):
    OPEN_POSITION_VALUE = 'open_position_value', _('open_position_value')
    CLOSE_POSITION_VALUE = 'close_position_value', _('close_position_value')
    TAKE_PROFIT_VALUE = 'take_profit_value', _('take_profit_value')
