from django.conf import settings

HOST = settings.BINANCE_CONFIG['host']
APIKEY = settings.BINANCE_CONFIG['api_key']
SECRET_KEY = settings.BINANCE_CONFIG['secret_key']
NEW_ORDER_ENDPOINT_FUTURE = settings.BINANCE_CONFIG['new_order_endpoint_future']
POSITION_INFORMATION = settings.BINANCE_CONFIG['position_information']
CHANGE_LEVERAGE = settings.BINANCE_CONFIG['change_leverage']
