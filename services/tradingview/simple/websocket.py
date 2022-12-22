import _thread
from time import sleep

from services.tradingview.core.base_socket import OpenWebsocketConnection
from services.tradingview.core.configs import resolve_sample_chart, get_strategy_str
from strategy.models import TradingViewStrategy


class WebSocketConnectionSampleChart(OpenWebsocketConnection):

    def __init__(self, instance: TradingViewStrategy):
        self.instance = instance
        super(WebSocketConnectionSampleChart, self).__init__(self.instance.symbol, self.instance.get_timeframe_display())
        self.strategy_settings = get_strategy_str(
            self.instance.pine_id,
            self.instance.pine_version,
            self.instance.script_mode
        )
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
        try:
            results = super(WebSocketConnectionSampleChart, self).on_message(ws, message)
            if results is None:
                return results
            for result in results:
                if result['m'] == 'du':
                    strategy_values = result['p'][1].get('st7')
                    if strategy_values:
                        strategy_values = strategy_values['st'][-1]['v']
                        date_time = strategy_values[0]
                        open_price = strategy_values[1]
                        tps = strategy_values[2:-1]
                        stop_lost = strategy_values[-1]
                        print(date_time, open_price, tps, stop_lost, sep=" -- ")
        except Exception as e:
            pass
        return result
