from dataclasses import dataclass
from typing import  List
from traffic_data_row import TrafficData

@dataclass
class user_history:
    rows: List[TrafficData]
