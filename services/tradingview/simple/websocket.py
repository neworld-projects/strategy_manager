import _thread
import logging
from time import sleep

from django.conf import settings

from services.tradingview.core.base_socket import OpenWebsocketConnection
from services.tradingview.core.configs import resolve_sample_chart, get_strategy_str
from strategy.DTOs import StateInformation, TpsValue, TelegramOpenPositionMessageBuilder
from strategy.models import TradingViewStrategy
from strategy.tasks.third_party import third_party_manager


class WebSocketConnectionSampleChart(OpenWebsocketConnection):

    def __init__(self, instance: TradingViewStrategy):
        self.instance = instance
        super(WebSocketConnectionSampleChart, self).__init__(self.instance.symbol,
                                                             self.instance.get_timeframe_display())
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
        logging.info("channel was opened")

        def self_setting():
            ws.send(resolve_sample_chart(self.symbol))
            super(WebSocketConnectionSampleChart, self).continue_opening(ws)
            ws.send(self.strategy_settings)

        _thread.start_new_thread(self_setting, ())

    def send_position_data(self, position_data: TelegramOpenPositionMessageBuilder):
        position_data = position_data.__dict__
        logging.info("open position data", extra={'info': position_data})
        third_party_manager.apply_async(
            args=(position_data, settings.TELEGRAM_MODULE),
            kwargs={'chat_id': self.instance.telegram_id}
        )
        if self.instance.broker_is_active:
            # TODO: send to broker
            pass

    def check_message(self, result):
        strategy_values = result['p'][1].get('st7')
        if strategy_values:
            strategy_values = strategy_values['st'][-1]['v']
            current_state = StateInformation(
                strategy_values[0],
                strategy_values[1],
                TpsValue(strategy_values[2:-1]),
                strategy_values[-1]
            )
            if current_state.datetime_timestamp != self.last_state.datetime_timestamp > 0 != self.last_state.open_position_value:
                position_data = TelegramOpenPositionMessageBuilder(self.last_state, current_state)
                self.send_position_data(position_data)
            self.last_state = current_state
            logging.info("last state", extra={'info': self.last_state.__dict__})

    def on_message(self, ws, message):
        try:
            results = super(WebSocketConnectionSampleChart, self).on_message(ws, message)
            if results is None:
                return results
            for result in results:
                if result.get('m') == 'du':
                    self.check_message(result)

        except Exception as e:
            logging.error(e)
