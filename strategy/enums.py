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
    def get_minute(cls, interval):
        if (
                interval == cls.ONE_HOUR or
                interval == cls.THREE_HOUR or
                interval == cls.THREE_HOUR or
                interval == cls.FOUR_HOUR or
                interval == cls.DAILY
        ):
            return 0
        return None

    @classmethod
    def get_hour(cls, interval):
        if (
                interval == cls.DAILY
        ):
            return 0
        return None

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
