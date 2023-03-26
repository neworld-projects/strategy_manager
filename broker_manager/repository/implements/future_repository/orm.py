from django.utils.datetime_safe import datetime
from multimethod import multimethod

from broker_manager.enums import PositionTypeChoice, PositionSideChoice
from broker_manager.models import PositionManager
from broker_manager.repository.abstracts.orm import AbstractFutureRepository


class ORMFutureRepository(AbstractFutureRepository):

    @multimethod
    def open_future_position(
            self,
            datetime_timestamp: str,
            price: float,
            position_side: PositionSideChoice,
            coin_name: str,
            quantity: float,
            position_type: PositionTypeChoice,
            start_send_to_broker_datetime: float,
            end_send_to_broker_datetime: float,
            broker_response_status_code: int,
            broker_response_message: str,
            request_from: str,
            request_id: int,
            broker: int,
            position_related: PositionManager = None,
    ) -> PositionManager:
        instance = PositionManager.objects.create(
            coin_name=coin_name,
            position_side=position_side,
            position_type=position_type,
            quantity=quantity,
            price=price,
            candle_datetime=datetime.fromtimestamp(float(datetime_timestamp)),
            start_send_to_broker_datetime=datetime.utcfromtimestamp(start_send_to_broker_datetime),
            end_send_to_broker_datetime=datetime.utcfromtimestamp(end_send_to_broker_datetime),
            broker_response_status_code=broker_response_status_code,
            broker_response_message=broker_response_message,
            request_from=request_from,
            request_id=request_id,
            broker=broker,
            position_related=position_related
        )
        return instance
