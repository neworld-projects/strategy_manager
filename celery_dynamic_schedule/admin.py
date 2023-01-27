from django.contrib import admin

# Register your models here.
from celery_dynamic_schedule.models import CeleryDynamicSchedule


@admin.register(CeleryDynamicSchedule)
class CoinDataAdmin(admin.ModelAdmin):
    list_display = ['name', ]
