import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapar.settings')

app = Celery('strategy_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.task_routes = {
    settings.TRADINGVIEW_STRATEGY_CHECK_TASK: {
        'queue': 'tradingview_strategy_check'
    }
}
