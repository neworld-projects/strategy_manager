from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class TpsValue:
    tps: list[float] = None

    def __dict__(self):
        return {f"tps{i}": self.tps[i] for i in range(self.tps.__len__())}


@dataclass
class StateInformation:
    datetime_timestamp: float = 0
    open_position_value: float = 0
    tps_value: TpsValue = TpsValue()
    close_position_value: float = 0


@dataclass
class TelegramOpenPositionMessageBuilder:
    datetime_timestamp: datetime
    open_position_value: float
    tps_value: TpsValue
    close_position_value: float
    position_mode: str

    def __init__(self, last_state: StateInformation, current_state: StateInformation):
        self.datetime_timestamp = datetime.utcfromtimestamp(current_state.datetime_timestamp)
        self.open_position_value = last_state.open_position_value
        self.tps_value = last_state.tps_value
        self.close_position_value = last_state.close_position_value
        self.position_mode = "long" if last_state.close_position_value > last_state.open_position_value else "short"

# TelegramOpenPositionMessageBuilder(StateInformation(41646, 131,[200,300,400],500), StateInformation(4146646, 0,[0,0,0],0))
