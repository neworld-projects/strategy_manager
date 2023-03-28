import logging
import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from celery.signals import task_failure
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapar.settings')

app = Celery('strategy_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')


@task_failure.connect
def task_failure_handler(sender=None, exception=None, args=None, **kwargs):
    logging.info(f'{sender.name} {exception}')


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check celery dynamic schedule': {
        'task': 'celery_dynamic_schedule.tasks.check_tasks_for_run',
        'options': {'queue': 'celery_dynamic_schedule'},
        'schedule': crontab('*')
    },

}
app.conf.task_routes = {
    settings.TRADINGVIEW_STRATEGY_CHECK_TASK: {
        'queue': 'tradingview_strategy_check'
    },
    settings.THIRD_PARTY_MANAGER_TASK: {
        'queue': 'third_party_manager'
    }
}
