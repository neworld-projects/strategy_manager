import _thread
import datetime
import logging
import platform
import re
from json import loads

import websocket
from django.conf import settings

from services.tradingview.core.configs import TradingViewConfig
from strategy.tasks.third_party import third_party_manager


logging.DEBUG = False


class OpenWebsocketConnection:
    def __init__(self, symbol: str, timeframe: str):
        self.timeframe = timeframe
        self.timeframe_for_send = loads(self.timeframe)
        self.config = TradingViewConfig(symbol, self.timeframe_for_send)
        self.symbol = symbol
        self.tradingview_websocket_url = settings.TRADINGVIEW_WEBSOCKET_URL
        websocket.enableTrace(True)
        self.ws_app = websocket.WebSocketApp(url=self.tradingview_websocket_url,
                                             header=self.config.headers,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             )

    def extra_on_open_messages(self):
        return []

    def on_message(self, ws, message):
        if re.search("~m~[0-9]+~m~~h~[0-9]+", message):
            ws.send(message)
            return None
        else:
            split_message = re.split("~m~[0-9]+~m~", message)
            list_json_message = []
            for convert in split_message[1:]:
                try:
                    list_json_message.append(loads(convert))
                except Exception as e:
                    logging.error(e)
            return list_json_message

    def on_error(self, ws, error):
        logging.error(error, extra={'info': {"timeframe": self.timeframe}})

    def on_close(self, ws, close_status_code, close_msg):
        logging.warning('close', extra={'info': {"timeframe": self.timeframe}})
        if not settings.DEVEL:
            third_party_manager.apply_async(
                args=({"message": "something want wrong",
                       "time": datetime.datetime.now(),
                       "symbol": self.symbol,
                       "hostname": platform.uname().node}, settings.TELEGRAM_MODULE),
                kwargs={'chat_id': settings.TELEGRAM_CHAT_ID_FOR_TRACK_PROBLEM}
            )

    def on_open(self, ws):
        def run(*args):
            ws.send(self.config.get_token_message)

            ws.send(self.config.get_chart_session_message)

            ws.send(self.config.get_switch_timezone_message)

            ws.send(self.config.get_quote_session_message)

            ws.send(self.config.get_add_symbols_message)

            ws.send(self.config.get_resolve_sample_chart_message)

            ws.send(self.config.get_create_series_message(300))

            for extra_on_open_message in self.extra_on_open_messages():
                ws.send(extra_on_open_message)

        _thread.start_new_thread(run, ())
