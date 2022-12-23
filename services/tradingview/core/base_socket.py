import _thread
import logging
import re
from json import loads

import websocket
from django.conf import settings

from services.tradingview.core.configs import token, chart_session, quote_session, add_symbols, headers, create_series, \
    switch_timezone

logging.DEBUG = False


class OpenWebsocketConnection:
    def __init__(self, symbol: str, timeframe: str):
        self.timeframe = timeframe
        self.timeframe_for_send = loads(self.timeframe)
        self.symbol = symbol
        self.tradingview_websocket_url = settings.TRADINGVIEW_WEBSOCKET_URL
        websocket.enableTrace(True)
        self.ws_app = websocket.WebSocketApp(url=self.tradingview_websocket_url,
                                             header=headers,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             )

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

    def on_open(self, ws):
        def run(*args):
            ws.send(token)

            ws.send(chart_session)

            ws.send(switch_timezone)

            ws.send(quote_session)

            ws.send(add_symbols(self.symbol))

        _thread.start_new_thread(run, ())

    def continue_opening(self, ws):
        ws.send(create_series(self.timeframe_for_send['name'], 300))
