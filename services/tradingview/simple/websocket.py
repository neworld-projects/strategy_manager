import _thread
from time import sleep

from django.conf import settings

from helpers.send_to_third_party import third_party_manager
from services.tradingview.core.base_socket import OpenWebsocketConnection
from services.tradingview.core.configs import resolve_sample_chart, get_strategy_str
from strategy.DTOs import StateInformation, TpsValue, TelegramOpenPositionMessageBuilder
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
        self.last_state = StateInformation()
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
                        current_state = StateInformation(
                            strategy_values[0],
                            strategy_values[1],
                            TpsValue(strategy_values[2:-1]),
                            strategy_values[-1]
                        )
                        if 0 < self.last_state.datetime_timestamp != current_state.datetime_timestamp \
                                and self.last_state.open_position_value != 0:
                            third_party_manager.apply_async(
                                args=(
                                    TelegramOpenPositionMessageBuilder(self.last_state, current_state).__dict__,
                                    settings.TELEGRAM_MODULE,
                                    True
                                ),
                                kwargs={'chat_id': self.instance.telegram_id}
                            )
                            # print(date_time, open_price, tps, stop_lost, sep=" -- ")
                        self.last_state = current_state

        except Exception as e:
            pass
        return result
