from django.contrib import admin

# Register your models here.
from broker_manager.models import PositionManager


@admin.register(PositionManager)
class CoinDataAdmin(admin.ModelAdmin):
    list_display = ['coin_name', 'position_type', 'position_side', 'request_from', 'request_id', 'broker',
                    'broker_response_status_code']
    list_filter = ['position_type', 'position_side', 'broker', 'broker_response_status_code']
    search_fields = ['coin_name', 'request_from', 'request_id']
