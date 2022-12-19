import _thread
from time import sleep

from services.tradingview.core.base_socket import OpenWebsocketConnection
from services.tradingview.core.configs import resolve_sample_chart


class WebSocketConnectionSampleChart(OpenWebsocketConnection):

    def __init__(self, symbol: str, timeframe: str, strategy_settings: str):
        super(WebSocketConnectionSampleChart, self).__init__(symbol, timeframe)
        self.strategy_settings = strategy_settings
        self.ws_app.run_forever()

    def on_open(self, ws):
        super(WebSocketConnectionSampleChart, self).on_open(ws)
        sleep(10)

        def self_setting():
            ws.send(resolve_sample_chart(self.symbol))
            super(WebSocketConnectionSampleChart, self).continue_opening(ws)
            ws.send(self.strategy_settings)

        _thread.start_new_thread(self_setting, ())

    def on_message(self, ws, message):
        result = super(WebSocketConnectionSampleChart, self).on_message(ws, message)
        if result is None:
            return result
        print(result)
        return result
