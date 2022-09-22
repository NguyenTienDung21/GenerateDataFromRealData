from dataclasses import dataclass
from typing import List

@dataclass
class Edge:
    id: str
    src: str
    dest: str
    attribute: List[str]