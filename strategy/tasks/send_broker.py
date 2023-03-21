import logging
from typing import List

from celery import shared_task
from django.conf import settings

from helpers.prepare_open_position import PrepareOpenPosition
from services.binance.send_request import SendRequest as SendRequestBinance
from strategy.tasks.third_party import third_party_manager


@shared_task(name=settings.SEND_BROKER)
def send_request_to_broker(
        coin_name: str,
        quantity: float,
        datetime_timestamp: str,
        open_position_value: float,
        tps: List[float],
        close_position_value: float,
        position_mode: str,
        request_from: str,
        request_id: int,
        telegram_id: str,
        leverage: int,
        margin_type: str,
        broker_name="binance"
):
    logging.info(f"tobe start instance")
    check = False
    check_prepare, message = PrepareOpenPosition(broker_name, coin_name, telegram_id).prepare_open_position(leverage,
                                                                                                            margin_type)
    if not check_prepare:
        message_data = message
    else:
        if broker_name == 'binance':
            check = SendRequestBinance().create_limit_position_with_tps_and_loss_in_future(
                coin_name,
                quantity,
                datetime_timestamp,
                open_position_value,
                tps,
                close_position_value,
                position_mode,
                request_from,
                request_id
            )

        if check:
            message_data = "successful send position"
        else:
            message_data = "something want wrong, some of positions can't open"

    third_party_manager.apply_async(
        args=({"message": message_data, "broker": broker_name}, settings.TELEGRAM_MODULE),
        kwargs={'chat_id': telegram_id}
    )
