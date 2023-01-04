from celery import shared_task

from celery_dynamic_schedule.utils import active_tasks


@shared_task
def check_tasks_for_run():
    active_tasks()
