from django.db import models


class PositionTypeChoice(models.IntegerChoices):
    LIMIT = 0, 'limit'
    MARKET = 1, 'market'
    STOP = 2, 'stop'
    TAKE_PROFIT = 3, 'take profit'
    STOP_MARKET = 4, 'stop market'
    TAKE_PROFIT_MARKET = 5, 'take profit market'
    TRAILING_STOP_MARKET = 6, 'trailing stop market'


class PositionSideChoice(models.IntegerChoices):
    LONG = 0, 'long'
    SHORT = 1, 'short'


class Broker(models.IntegerChoices):
    BINANCE = 0, 'binance'
