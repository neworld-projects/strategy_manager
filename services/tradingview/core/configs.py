import json

from django.conf import settings

headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    "origin": "https://www.tradingview.com",

}

token = '~m~525~m~{"m":"set_auth_token","p":["' + settings.AUTH_TOKEN + '"]}'
chart_session = '~m~55~m~{"m":"chart_create_session","p":["' + settings.CS_TOKEN + '",""]}'
quote_session = '~m~52~m~{"m":"quote_create_session","p":["' + settings.QS_TOKEN + '"]}'


def add_symbols(name):
    return '~m~142~m~{"m":"quote_add_symbols","p":["' + settings.QS_TOKEN + '","={\\"symbol\\":\\"' + \
           f'BINANCE:{name.upper()}' + '\\",\\"adjustment\\":\\"splits\\"}",{"flags":["force_permission"]}]}'


def resolve_sample_chart(name):
    return '~m~120~m~{"m":"resolve_symbol","p":["' + settings.CS_TOKEN + '","sds_sym_1","={\\"symbol\\":\\"' + \
           f'BINANCE:{name.upper()}' + '\\",\\"adjustment\\":\\"splits\\"}"]}'


def resolve_heikin_ashi_chart(name):
    return '~m~197~m~{"m":"resolve_symbol","p":["' + settings.CS_TOKEN + '","sds_sym_1","={\\"symbol\\":{\\"symbol\\":\\"' + \
           f'BINANCE:{name.upper()}' + '\\",\\"adjustment\\":\\"splits\\"},\\"type\\":\\"BarSetHeikenAshi@tv-basicstudies-60!\\",\\"inputs\\":{}}"]}'


def create_series(timeframe: str, length: int):
    if timeframe == "120" or timeframe == "180" or timeframe == "240":
        request_number = 83
    elif timeframe == '5':
        request_number = 81
    else:
        request_number = 82
    return '~m~' + str(
        request_number) + '~m~{"m":"create_series","p":["' + settings.CS_TOKEN + '","sds_1","s1","sds_sym_1","' + \
           str(timeframe) + '",' + str(length) + ',""]}'


def more_data(length: int):
    return '~m~62~m~{"m":"request_more_data","p":["' + settings.CS_TOKEN + '","sds_1",' + str(length) + ']}'


def get_strategy_str(strategy_settings: dict):
    setting_dictionary = [
        {
            'm': 'create_study',
            'p': [
                settings.CS_TOKEN,
                'st7',
                'st1',
                'sds_1',
                'StrategyScript@tv-scripting-101!',
                strategy_settings
            ]
        }
    ]
    return f'~m~6135~m~{json.dumps(setting_dictionary)}'
