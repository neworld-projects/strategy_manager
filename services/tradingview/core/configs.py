import json
import logging
from collections import ChainMap

import requests
from django.conf import settings

from strategy.enums import TradingViewScriptModeChoice

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
switch_timezone = '~m~57~m~{"m":"switch_timezone","p":["' + settings.CS_TOKEN + '","Etc/UTC"]}'
quote_session = '~m~52~m~{"m":"quote_create_session","p":["' + settings.QS_TOKEN + '"]}'


def add_symbols(name):
    return '~m~168~m~{"m":"quote_add_symbols","p":["' + settings.QS_TOKEN + '","={\\"adjustment\\":\\"splits\\",\\"currency-id\\":\\"XTVCUSDT\\",\\"session\\":\\"regular\\",\\"symbol\\":\\"BINANCE:' + name.upper() + '\\"}"]}'


def resolve_sample_chart(name):
    return '~m~177~m~{"m":"resolve_symbol","p":["' + settings.CS_TOKEN + '","sds_sym_1","={\\"adjustment\\":\\"splits\\",\\"currency-id\\":\\"XTVCUSDT\\",\\"session\\":\\"regular\\",\\"symbol\\":\\"BINANCE:' + name.upper() + '\\"}"]}'

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


class InputDataFrame(object):
    def __init__(self, value):
        if value.get('isFake'):
            self.value = {
                value.get('id'): {
                    'v': value.get('defval'),
                    'f': value.get('isFake'),
                    't': value.get('type'),
                }
            }
        else:
            self.value = {
                value.get('id'): value.get('defval')
            }

    @property
    def __dict__(self):
        return self.value


def get_indicator(indicator_id: str, indicator_version: str):
    url = f'https://pine-facade.tradingview.com/pine-facade/translate/USER;{indicator_id}/{indicator_version}/?user_name={settings.TRADINGVIEW_USERNAME}'
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': 'https://www.tradingview.com',
        'referer': 'https://www.tradingview.com/'
    }
    response = requests.get(url, headers=headers).json()
    result = dict(
        ChainMap(*[
            {'text': response['result']['ilTemplate']},
            *[InputDataFrame(data).__dict__ for data in response['result']['metaInfo']['inputs'][::-1]]
        ])
    )
    result['pineVersion'] = indicator_version
    result['pineId'] = f'USER;{indicator_id}'
    return result


def get_strategy_str(pine_id, pine_version, script_mode):
    setting_dictionary = {
        'm': 'create_study',
        'p': [
            settings.CS_TOKEN,
            'st7',
            'st1',
            'sds_1',
            'Script@tv-scripting-101!'
            if script_mode == TradingViewScriptModeChoice.INDICATOR
            else 'StrategyScript@tv-scripting-101!',
            get_indicator(pine_id, pine_version)
        ]
    }
    data = f'~m~2606~m~{json.dumps(setting_dictionary)}'.replace(" ", '')
    logging.info(f"ready message for send {data}")
    return data
