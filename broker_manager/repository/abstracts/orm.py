from abc import ABC

from multimethod import multimethod

from broker_manager.enums import PositionTypeChoice
from broker_manager.models import PositionManager


class AbstractFutureRepository(ABC):

    @multimethod
    def open_future_position(
            self,
            datetime_timestamp: str,
            price: float,
            position_mode: str,
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
        raise NotImplemented
