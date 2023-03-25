import logging

from django.conf import settings

from services.tradingview.core.base_socket import OpenWebsocketConnection
from strategy.DTOs import StateInformation, OpenPositionMessageBuilder
from strategy.models import TradingViewStrategy
from strategy.tasks.send_broker import send_request_to_broker
from strategy.tasks.third_party import third_party_manager


class WebSocketConnectionChartForStrategyManager(OpenWebsocketConnection):

    def __init__(self, instance: TradingViewStrategy):
        self.strategy_settings = None
        self.instance = instance

        super(WebSocketConnectionChartForStrategyManager, self).__init__(
            self.instance.symbol,
            self.instance.get_timeframe_display(),
        )
        self.strategy_model = instance.strategy_model
        self.last_state = StateInformation()
        self.ws_app.run_forever()

    def extra_on_open_messages(self):
        self.strategy_settings = self.config.get_strategy_message(
            self.instance.pine_id,
            self.instance.pine_version,
            self.instance.script_mode
        )
        return [self.strategy_settings, ]

    def send_position_data(self, position_data: OpenPositionMessageBuilder):
        position_data_dict = position_data.__dict__
        logging.info(f"open position data {position_data_dict}")
        if not settings.DEVEL:
            third_party_manager.apply_async(
                args=(position_data_dict, settings.TELEGRAM_MODULE),
                kwargs={'chat_id': self.instance.telegram_id}
            )
            if self.instance.broker_is_active:
                send_request_to_broker.apply_async(
                    (
                        self.instance.symbol,
                        self.instance.base_capital,
                        position_data_dict,
                        self.instance._meta.db_table,
                        self.instance.id,
                        self.instance.telegram_id,
                        self.instance.leverage,
                        self.instance.get_margin_type_display(),
                    ),
                    expires=60
                )

    def check_message(self, result):
        strategy_values = result['p'][1].get('st7')
        if strategy_values:
            strategy_values = strategy_values['st'][-1]['v']
            current_state = StateInformation(
                strategy_values[0],
                strategy_values[1:-2],
                "long" if strategy_values[-2] == 1 else "short" if strategy_values[-2] == -1 else "",
                strategy_values[-1]
            )
            if current_state > self.last_state and self.last_state:
                position_data = OpenPositionMessageBuilder(self.last_state, current_state, self.strategy_model)
                self.send_position_data(position_data)
            self.last_state = current_state
            logging.info(f"last state {self.last_state.__dict__}")

    def on_message(self, ws, message):
        try:
            results = super(WebSocketConnectionChartForStrategyManager, self).on_message(ws, message)
            if results is None:
                return results
            for result in results:
                if result.get('m') == 'du':
                    self.check_message(result)

        except Exception as e:
            logging.error(e)
