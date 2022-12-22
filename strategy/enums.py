from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import IntervalSchedule


class TimeInterval(models.TextChoices):
    ONE_MIN = 'one_min', _('1 min')
    FIVE_MIN = 'five_min', _('5 min')
    ONE_HOUR = 'one_hour', _('1 hour')
    TWO_HOUR = 'two_hour', _('2 hour')
    THREE_HOUR = 'three_hour', _('3 hour')
    FOUR_HOUR = 'four_hour', _('4 hour')
    DAILY = 'one_day', _('1 day')

    @classmethod
    def get_second(cls, interval):
        if (
                interval == cls.ONE_MIN or
                interval == cls.FIVE_MIN
        ):
            return 55
        return None

    @classmethod
    def get_minute(cls, interval):
        if (
                interval == cls.ONE_HOUR or
                interval == cls.THREE_HOUR or
                interval == cls.THREE_HOUR or
                interval == cls.FOUR_HOUR or
                interval == cls.DAILY
        ):
            return 55
        return None

    @classmethod
    def get_hour(cls, interval):
        if (
                interval == cls.DAILY
        ):
            return 23
        return None

    @classmethod
    def get_replace_args(cls, interval):
        minute = cls.get_minute(interval)
        hour = cls.get_hour(interval)
        second = cls.get_second(interval)

        result = {'microsecond': 0}
        if minute:
            result['minute'] = minute
        if hour:
            result['hour'] = hour
        if second:
            result['second'] = second
        return result

    @classmethod
    def convert_to_interval_model(cls, interval):
        if cls.ONE_MIN == interval:
            return IntervalSchedule.objects.get_or_create(every=1, period='minutes')

        if cls.FIVE_MIN == interval:
            return IntervalSchedule.objects.get_or_create(every=5, period='minutes')

        if cls.ONE_HOUR == interval:
            return IntervalSchedule.objects.get_or_create(every=1, period='hours')

        if cls.TWO_HOUR == interval:
            return IntervalSchedule.objects.get_or_create(every=2, period='hours')

        if cls.THREE_HOUR == interval:
            return IntervalSchedule.objects.get_or_create(every=3, period='hours')

        if cls.FOUR_HOUR == interval:
            return IntervalSchedule.objects.get_or_create(every=4, period='hours')

        if cls.DAILY == interval:
            return IntervalSchedule.objects.get_or_create(every=1, period='days')


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
