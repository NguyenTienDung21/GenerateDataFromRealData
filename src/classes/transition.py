import json
from dataclasses import dataclass
from typing import List
from classes.variable import Variable

@dataclass
class Transition:
    edge_id: str
    variables: List[Variable]

    def __repr__(self):
        return json.dumps({
            "edgeid": self.edge_id,
            "variable": json.loads(str(self.variables))
        })
