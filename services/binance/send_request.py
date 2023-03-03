import hashlib
import hmac
import json
from typing import List
from urllib.parse import urljoin, urlencode

import requests
from django.utils.datetime_safe import datetime

from broker_manager.enums import PositionTypeChoice, Broker, PositionSideChoice
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

    def send_post(self, endpoint: str, data: dict) -> (bool, int, dict, datetime, datetime):
        start = datetime.now()
        response = requests.post(
            url=urljoin(HOST, endpoint),
            headers=self.headers,
            json=data,

        )
        end = datetime.now()
        return response.ok, response.status_code, response.json(), start, end

    def create_limit_position_with_tps_and_loss_in_future(
            self,
            coin_name: str,
            quantity: int,
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
        # TODO: change quantity value to percentage
        check, status_code, message, start, end = self.send_post(
            NEW_ORDER_ENDPOINT_FUTURE,
            {
                "symbol": coin_name,
                "side": "BUY",
                "positionSide": position_mode.name,
                "type": "LIMIT",
                "quantity": quantity,
                "price": open_position_value,
            }
        )
        check_list.append(check)
        base_position = BrokerManagerRepository().open_future_position(
            datetime_timestamp,
            open_position_value,
            position_mode,
            coin_name,
            quantity,
            PositionTypeChoice.LIMIT,
            start,
            end,
            status_code,
            json.dumps(message),
            request_from,
            request_id,
            Broker.BINANCE.value
        )
        for tp in tps:
            check, status_code, message, start, end = self.send_post(
                NEW_ORDER_ENDPOINT_FUTURE,
                {
                    "symbol": coin_name,
                    "side": "SELL",
                    "positionSide": position_mode.name,
                    "type": "TAKE_PROFIT",
                    "quantity": quantity / len(tps),
                    "price": tp,
                    "stopPrice": tp
                }
            )
            check_list.append(check)
            BrokerManagerRepository().open_future_position(
                datetime_timestamp,
                tp,
                position_mode,
                coin_name,
                quantity,
                PositionTypeChoice.TAKE_PROFIT,
                start,
                end,
                status_code,
                json.dumps(message),
                request_from,
                request_id,
                Broker.BINANCE.value,
                base_position
            )
        check, status_code, message, start, end = self.send_post(
            NEW_ORDER_ENDPOINT_FUTURE,
            {
                "symbol": coin_name,
                "side": "SELL",
                "positionSide": position_mode.name,
                "type": "STOP",
                "quantity": quantity,
                "price": close_position_value,
                "stopPrice": close_position_value
            }
        )
        check_list.append(check)
        BrokerManagerRepository().open_future_position(
            datetime_timestamp,
            close_position_value,
            position_mode,
            coin_name,
            quantity,
            PositionTypeChoice.STOP,
            start,
            end,
            status_code,
            json.dumps(message),
            request_from,
            request_id,
            Broker.BINANCE.value,
            base_position
        )
        return all(check_list)
