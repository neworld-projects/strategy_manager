from django.db import models


# Create your models here.
class CeleryDynamicSchedule(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    task = models.CharField(max_length=150)
    task_args = models.JSONField(default=dict)
    last_run = models.DateTimeField(null=True, blank=True)
    crontab_code = models.CharField(max_length=150)
    run_crontab_minute = models.JSONField(default=dict)
    run_crontab_hour = models.JSONField(default=dict)
    run_crontab_day_of_week = models.JSONField(default=dict)
    run_crontab_day_of_month = models.JSONField(default=dict)
    run_crontab_month_of_year = models.JSONField(default=dict)
