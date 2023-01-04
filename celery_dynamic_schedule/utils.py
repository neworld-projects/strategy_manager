import datetime

from celery_dynamic_schedule.models import CeleryDynamicSchedule
from strategy_manager.celery import app


def active_tasks():
    now_datetime = datetime.datetime.now().replace(second=0, microsecond=0)
    active_tasks_for_run = CeleryDynamicSchedule.objects.filter(
        **{
            f"run_crontab_minute__{now_datetime.minute}n": now_datetime.minute,
            f"run_crontab_hour__{now_datetime.hour}n": now_datetime.hour,
            f"run_crontab_day_of_week__{now_datetime.weekday()}n": now_datetime.weekday(),
            f"run_crontab_day_of_month__{now_datetime.day}n": now_datetime.day,
            f"run_crontab_month_of_year__{now_datetime.month}n": now_datetime.month,
        }
    )
    for active_task in active_tasks_for_run:
        app.send_task(active_task.task, args=list(active_task.task_args))
