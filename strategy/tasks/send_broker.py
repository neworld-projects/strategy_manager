import logging
from typing import List

from celery import shared_task
from django.conf import settings

from services.binance.send_request import SendRequest as SendRequestBinance


@shared_task(name=settings.SEND_BROKER)
def send_request_to_broker(
        coin_name: str,
        quantity: int,
        datetime_timestamp: str,
        open_position_value: float,
        tps: List[float],
        close_position_value: float,
        position_mode: str,
        request_from: str,
        request_id: int,
        broker_name="binance"
):
    logging.info(f"tobe start instance")
    if broker_name == 'binance':
        SendRequestBinance().create_limit_position_with_tps_and_loss_in_future(
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
