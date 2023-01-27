from django.apps import AppConfig


class CeleryDynamicScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_dynamic_schedule'

    def ready(self):
        from . import signals