from django.conf import settings

HOST = settings.BINANCE_CONFIG['host']
APIKEY = settings.BINANCE_CONFIG['api_key']
SECRET_KEY = settings.BINANCE_CONFIG['secret_key']
NEW_ORDER_ENDPOINT_FUTURE = settings.BINANCE_CONFIG['new_order_endpoint_future']
