import _thread
from time import sleep

from services.tradingview.core.base_socket import OpenWebsocketConnection
from services.tradingview.core.configs import resolve_sample_chart, get_strategy_str
from strategy.models import TradingViewStrategy


class WebSocketConnectionSampleChart(OpenWebsocketConnection):

    def __init__(self, instance: TradingViewStrategy):
        self.instance = instance
        super(WebSocketConnectionSampleChart, self).__init__(self.instance.symbol, self.instance.get_timeframe_display())
        self.strategy_settings = get_strategy_str(self.instance.settings)
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
        if result['m'] == 'du':
            strategy_values = result['m'][1].get('st7')
            if strategy_values:
                date_time = strategy_values[0]
                open_price = strategy_values[1]
                tps = strategy_values[2:-1]
                stop_lost = strategy_values[-1]
                print(date_time, open_price, tps, stop_lost, sep=" -- ")
        return result
