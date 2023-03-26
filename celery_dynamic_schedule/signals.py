import json

from celery.schedules import crontab
from django.db.models.signals import pre_save
from django.dispatch import receiver

from celery_dynamic_schedule.models import CeleryDynamicSchedule


@receiver(pre_save, sender=CeleryDynamicSchedule)
def create_crontab_schedule(sender, instance: CeleryDynamicSchedule, **kwargs):
    schedule = instance.crontab_code.split(" ")
    schedule = crontab(minute=schedule[0], hour=schedule[1], day_of_week=schedule[2], day_of_month=schedule[3], month_of_year=schedule[4])
    instance.run_crontab_minute = {f"{j}n": j if list(schedule.minute).count(j) else k for j, k in {i: None for i in range(60)}.items()}
    instance.run_crontab_hour = {f"{j}n": j if list(schedule.hour).count(j) else k for j, k in {i: None for i in range(24)}.items()}
    instance.run_crontab_day_of_week = {f"{j}n": j if list(schedule.day_of_week).count(j) else k for j, k in {i: None for i in range(0, 8)}.items()}
    instance.run_crontab_day_of_month = {f"{j}n": j if list(schedule.day_of_month).count(j) else k for j, k in {i: None for i in range(1, 32)}.items()}
    instance.run_crontab_month_of_year = {f"{j}n": j if list(schedule.month_of_year).count(j) else k for j, k in {i: None for i in range(1, 13)}.items()}
