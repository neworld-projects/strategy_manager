import hashlib
import hmac
import json
from typing import List
from urllib.parse import urljoin, urlencode

import requests
from django.utils.datetime_safe import datetime

from broker_manager.enums import PositionTypeChoice, Broker, PositionSideChoice
from broker_manager.models import PositionManager
from broker_manager.repository.broker_manager_repository import BrokerManagerRepository
from services.binance.settings import HOST, APIKEY, NEW_ORDER_ENDPOINT_FUTURE


class SendRequest:
    @property
    def __headers(self) -> dict:
        return {
            "X-MBX-APIKEY": APIKEY
        }

    @staticmethod
    def __add_signature_and_timestamp(data: dict) -> dict:
        data['timestamp'] = int(datetime.now().timestamp())
        data['signature'] = hmac.new(
            bytes("2b5eb11e18796d12d88f13dc27dbbd02c2cc51ff7059765ed9821957d82bb4d9", 'latin-1'),
            msg=bytes(urlencode(data), 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return data

    def __send_post(self, endpoint: str, data: dict) -> (bool, int, dict, datetime, datetime):
        start = datetime.now()
        response = requests.post(
            url=urljoin(HOST, endpoint),
            headers=self.__headers,
            json=data,

        )
        end = datetime.now()
        return response.ok, response.status_code, response.json(), start, end

    def __send_and_save(
            self,
            coin_name: str,
            position_mode: PositionSideChoice,
            quantity: float,
            open_position_value: float,
            side: str,
            datetime_timestamp: str,
            request_from: str,
            request_id: int,
            position_type: PositionTypeChoice,
            position_instance=None
    ) -> (PositionManager, bool):
        body = {
            "symbol": coin_name,
            "side": side,
            "positionSide": position_mode.name,
            "type": position_type.name,
            "quantity": quantity,
            "price": open_position_value,
        }
        if side == "SELL":
            body['stopPrice'] = open_position_value

        check, status_code, message, start, end = self.__send_post(NEW_ORDER_ENDPOINT_FUTURE, body)
        position = BrokerManagerRepository().open_future_position(
            datetime_timestamp,
            open_position_value,
            position_mode,
            coin_name,
            quantity,
            position_type,
            start,
            end,
            status_code,
            json.dumps(message),
            request_from,
            request_id,
            Broker.BINANCE.value,
            position_instance
        )
        return position, check

    def create_limit_position_with_tps_and_loss_in_future(
            self,
            coin_name: str,
            quantity: float,
            datetime_timestamp: str,
            open_position_value: float,
            tps: List[float],
            close_position_value: float,
            position_mode: str,
            request_from: str,
            request_id: int
    ) -> bool:

        position_mode = PositionSideChoice.LONG if position_mode == "long" else PositionSideChoice.SHORT
        check_list = []
        base_position_instance, check = self.__send_and_save(coin_name, position_mode, quantity, open_position_value,
                                                             "BUY", datetime_timestamp, request_from, request_id,
                                                             PositionTypeChoice.LIMIT)
        check_list.append(check)

        for tp in tps:
            position_instance, check = self.__send_and_save(coin_name, position_mode, quantity / len(tps), tp, "SELL",
                                                            datetime_timestamp, request_from, request_id,
                                                            PositionTypeChoice.TAKE_PROFIT, base_position_instance)
            check_list.append(check)

        if close_position_value != 0:
            position_instance, check = self.__send_and_save(coin_name, position_mode, quantity, close_position_value,
                                                            "SELL", datetime_timestamp, request_from, request_id,
                                                            PositionTypeChoice.STOP, base_position_instance)
            check_list.append(check)

        return all(check_list)
