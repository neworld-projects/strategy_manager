from dataclasses import dataclass, field
from datetime import datetime


# @dataclass
# class TpsValue:
#     tps: list[float] = None
#
#     @property
#     def __dict__(self):
#         return {f"tps{i}": self.tps[i] for i in range(self.tps.__len__())}


@dataclass
class StateInformation:
    datetime_timestamp: float = 0
    position_datas: list = field(default_factory=list)
    position_mode: str = ''
    last_open_position_value: float = 0

    def __gt__(self, other):
        if self.datetime_timestamp != other.datetime_timestamp > 0:
            return True
        return False

    def __bool__(self):
        return any(self.position_datas)


@dataclass
class OpenPositionMessageBuilder:
    datetime_timestamp: str
    position_object: dict
    position_mode: str
    last_open_position_value: float

    @staticmethod
    def convert_position_data_to_object(position_data: list, strategy_model: dict) -> dict:
        final_position_object = {}
        for key, value in strategy_model.items():
            final_position_object[value] = position_data[int(key)]
        return final_position_object

    def __init__(self, last_state: StateInformation, current_state: StateInformation, strategy_model: dict):
        self.datetime_timestamp = datetime.utcfromtimestamp(current_state.datetime_timestamp).__str__()
        self.position_object = self.convert_position_data_to_object(last_state.position_datas, strategy_model)
        self.position_mode = last_state.position_mode
        self.last_open_position_value = last_state.last_open_position_value

    @property
    def __dict__(self):
        return {
            "datetime_timestamp": self.datetime_timestamp,
            **self.position_object,
            "position_mode": self.position_mode,
            "last_open_position_value": self.last_open_position_value
        }
