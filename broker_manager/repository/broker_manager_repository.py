from django.utils.datetime_safe import datetime
from multimethod import multimethod

from broker_manager.enums import PositionTypeChoice
from broker_manager.models import PositionManager
from broker_manager.repository.abstracts.orm import AbstractFutureRepository
from broker_manager.repository.implements.future_repository.orm import ORMFutureRepository


class BrokerManagerRepository(AbstractFutureRepository):
    def __init__(self):
        self.future_implement = ORMFutureRepository()

    @multimethod
    def open_future_position(
            self,
            datetime_timestamp: str,
            price: float,
            position_mode: str,
            coin_name: str,
            quantity: float,
            position_type: PositionTypeChoice,
            start_send_to_broker_datetime: datetime,
            end_send_to_broker_datetime: datetime,
            broker_response_status_code: int,
            broker_response_message: str,
            request_from: str,
            request_id: int,
            broker: int,
            position_related: PositionManager = None,
    ) -> PositionManager:

        return self.future_implement.open_future_position(
            datetime_timestamp,
            price,
            position_mode,
            coin_name,
            quantity,
            position_type,
            start_send_to_broker_datetime,
            end_send_to_broker_datetime,
            broker_response_status_code,
            broker_response_message,
            request_from,
            request_id,
            broker,
            position_related,
        )
