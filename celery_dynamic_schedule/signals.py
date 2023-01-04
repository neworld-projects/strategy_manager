import json

from celery.schedules import crontab
from django.db.models.signals import post_save
from django.dispatch import receiver

from celery_dynamic_schedule.models import CeleryDynamicSchedule


@receiver(post_save, sender=CeleryDynamicSchedule)
def create_periodic_task(sender, instance: CeleryDynamicSchedule, **kwargs):
    schedule = crontab(instance.crontab_code)
    instance.run_crontab_minute = json.dumps(
        {j: j if list(schedule.minute).count(j) else k for j, k in {i: None for i in range(60)}.items()}
    )
    instance.run_crontab_hour = json.dumps(
        {j: j if list(schedule.hour).count(j) else k for j, k in {i: None for i in range(24)}.items()}
    )
    instance.run_crontab_day_of_week = json.dumps(
        {j: j if list(schedule.day_of_week).count(j) else k for j, k in {i: None for i in range(7)}.items()}
    )
    instance.run_crontab_day_of_month = json.dumps(
        {j: j if list(schedule.day_of_month).count(j) else k for j, k in {i: None for i in range(31)}.items()}
    )
    instance.run_crontab_month_of_year = json.dumps(
        {j: j if list(schedule.month_of_year).count(j) else k for j, k in {i: None for i in range(12)}.items()}
    )
    instance.save()
