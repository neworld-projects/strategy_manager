from django.contrib import admin

# Register your models here.
from strategy.models import TradingViewStrategy


@admin.register(TradingViewStrategy)
class CoinDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'running_interval', 'symbol', 'timeframe', 'is_active', 'base_capital']
    list_filter = ['is_active', 'timeframe', 'running_interval']
    search_fields = ['name', 'name']
