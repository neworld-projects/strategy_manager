import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapar.settings')

app = Celery('strategy_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check celery dynamic schedule': {
        'celery_dynamic_schedule.task.check_tasks_for_run': {
            'queue': 'celery_beat',
            'schedule': crontab('*')
        },
    }
}
app.conf.task_routes = {
    settings.TRADINGVIEW_STRATEGY_CHECK_TASK: {
        'queue': 'tradingview_strategy_check'
    },
    settings.THIRD_PARTY_MANAGER_TASK: {
        'queue': 'third_party_manager'
    }
}
