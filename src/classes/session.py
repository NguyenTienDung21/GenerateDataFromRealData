from dataclasses import dataclass
from typing import List

from classes.traffic_data_row import TrafficData

@dataclass
class Session:
    session_id: str
    history: List[TrafficData]

    def __repr__(self):
        return self.session_id
