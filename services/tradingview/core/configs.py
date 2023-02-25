import json
import logging
from collections import ChainMap
from typing import List

import requests
from django.conf import settings

from strategy.enums import TradingViewScriptModeChoice


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


class TradingViewConfig:
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "origin": "https://www.tradingview.com",
    }

    def __init__(self, name: str, timeframe: str):
        self.name = name.upper()
        self.timeframe = timeframe

    @staticmethod
    def convert_to_str_send_message(message: dict) -> str:
        message = json.dumps(message).replace(" ", '')
        return f'~m~{message.__len__()}~m~{message}'

    @staticmethod
    def build_message(m: str, p: List) -> dict:
        return {"m": m, "p": p}

    @staticmethod
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

    def compile_message(self, m: str, p: List) -> str:
        return self.convert_to_str_send_message(self.build_message(m, p))

    @property
    def get_token_message(self) -> str:
        m = "set_auth_token"
        p = [settings.AUTH_TOKEN, ]
        return self.compile_message(m, p)

    @property
    def get_chart_session_message(self) -> str:
        m = "chart_create_session"
        p = [settings.CS_TOKEN, ""]
        return self.compile_message(m, p)

    @property
    def get_switch_timezone_message(self) -> str:
        m = "switch_timezone"
        p = [settings.CS_TOKEN, "Etc/UTC"]
        return self.compile_message(m, p)

    @property
    def get_quote_session_message(self) -> str:
        m = "quote_create_session"
        p = [settings.QS_TOKEN, ]
        return self.compile_message(m, p)

    @property
    def get_add_symbols_message(self) -> str:
        m = "quote_add_symbols"
        extra1 = {
            "adjustment": "splits",
            "currency-id": "XTVCUSDT",
            "session": "regular",
            "symbol": f"BINANCE:{self.name}"
        }
        p = [settings.QS_TOKEN, f"={json.dumps(extra1)}"]
        return self.compile_message(m, p)

    @property
    def get_resolve_sample_chart_message(self) -> str:
        m = "resolve_symbol"
        extra1 = {
            "adjustment": "splits",
            "currency-id": "XTVCUSDT",
            "session": "regular",
            "symbol": f"BINANCE:{self.name}"
        }
        p = [settings.CS_TOKEN, 'sds_sym_1', f"={json.dumps(extra1)}"]
        return self.compile_message(m, p)

    @property
    def get_resolve_heikinashi_chart_message(self) -> str:
        m = "resolve_symbol"
        extra1 = {
            "symbol": {
                "symbol": f"BINANCE:{self.name}",
                "adjustment": "splits"
            },
            "type": "BarSetHeikenAshi@tv-basicstudies-60!",
            "inputs": {}
        }
        p = [settings.CS_TOKEN, 'sds_sym_1', f"={json.dumps(extra1)}"]
        return self.compile_message(m, p)

    def get_create_series_message(self, length: int) -> str:
        m = "create_series"
        p = [settings.CS_TOKEN, "sds_1", "s1", "sds_sym_1", self.timeframe, str(length)]
        return self.compile_message(m, p)

    def get_more_data_message(self, length: int) -> str:
        m = "request_more_data"
        p = [settings.CS_TOKEN, "sds_1", str(length)]
        return self.compile_message(m, p)

    def get_strategy_message(self, pine_id, pine_version, script_mode) -> str:
        m = 'create_study'
        p = [
            settings.CS_TOKEN,
            'st7',
            'st1',
            'sds_1',
            'Script@tv-scripting-101!'
            if script_mode == TradingViewScriptModeChoice.INDICATOR
            else 'StrategyScript@tv-scripting-101!',
            self.get_indicator(pine_id, pine_version)
        ]
        return self.compile_message(m, p)
