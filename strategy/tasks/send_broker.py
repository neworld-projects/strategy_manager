import logging

from celery import shared_task
from django.conf import settings

from broker_manager.enums import PositionSideChoice
from helpers.prepare_open_position import PrepareOpenPosition
from services.binance.send_request import SendRequest as SendRequestBinance
from strategy.tasks.third_party import third_party_manager


@shared_task(name=settings.SEND_BROKER)
def send_request_to_broker(
        coin_name: str,
        quantity: int,
        position_object: dict,
        request_from: str,
        request_id: int,
        telegram_id: str,
        leverage: int,
        margin_type: str,
        broker_name: str
):
    logging.info(f"tobe start instance")
    check = False
    clear = False
    if position_object.get("open_position_value") and position_object.get("open_position_value") != 0:
        clear = True
    check_prepare, message = PrepareOpenPosition(
        broker_name,
        coin_name,
        telegram_id,
        clear
    ).prepare_open_position(
        leverage,
        margin_type
    )
    if not check_prepare:
        message_data = message
    else:
        if broker_name == 'binance':
            datetime_timestamp = position_object.pop('datetime_timestamp')
            position_mode = PositionSideChoice.LONG \
                if position_object.pop('position_mode') == "long" \
                else PositionSideChoice.SHORT
            last_open_position_value = position_object.pop('last_open_position_value')
            total_profit = [keys for keys in position_object.keys() if keys.find("take_profit_value")].__len__()
            check_list = []
            for key, value in position_object:
                if key.find("open_position_value") != -1 and value != 0:
                    position_status = SendRequestBinance().buy_position(
                        coin_name,
                        quantity / value,
                        datetime_timestamp,
                        value,
                        position_mode,
                        request_from,
                        request_id
                    )
                    check_list.append(position_status)
                elif key.find("close_position_value") != -1:
                    position_status = SendRequestBinance().sell_position(
                        coin_name,
                        quantity / last_open_position_value,
                        datetime_timestamp,
                        value,
                        position_mode,
                        request_from,
                        request_id
                    )
                    check_list.append(position_status)
                elif key.find("take_profit_value") != -1:
                    position_status = SendRequestBinance().sell_position(
                        coin_name,
                        quantity / last_open_position_value / total_profit,
                        datetime_timestamp,
                        value,
                        position_mode,
                        request_from,
                        request_id
                    )
                    check_list.append(position_status)
            check = all(check_list)

        if check:
            message_data = "successful send position"
        else:
            message_data = "something want wrong, some of positions can't open"

    third_party_manager.apply_async(
        args=({"message": message_data, "broker": broker_name}, settings.TELEGRAM_MODULE),
        kwargs={'chat_id': telegram_id}
    )
