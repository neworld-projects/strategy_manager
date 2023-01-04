from django.contrib import admin

# Register your models here.
from strategy.models import TradingViewStrategy


@admin.register(TradingViewStrategy)
class CoinDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'crontab_code', 'symbol', 'timeframe', 'is_active', 'base_capital']
    list_filter = ['is_active', 'timeframe', 'crontab_code', 'script_mode']
    search_fields = ['name', 'name', 'pine_id']
