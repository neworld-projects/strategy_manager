import logging
from typing import List

from celery import shared_task
from django.conf import settings

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
        broker_name="binance"
):
    logging.info(f"tobe start instance")
    check = False
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
        message_data = {"message": "successful send position", "broker": broker_name}
    else:
        message_data = {"message": "something want wrong, some of positions can't open", "broker": broker_name}

    third_party_manager.apply_async(
        args=(message_data, settings.TELEGRAM_MODULE),
        kwargs={'chat_id': telegram_id}
    )
