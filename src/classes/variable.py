from dataclasses import dataclass
import json

@dataclass
class Variable:
    name: str
    type: str = None

    def __repr__(self):
        return json.dumps({
            "name": self.name,
            "recommendFormat": self.type
        })

@dataclass
class VariableData:
    name: str
    value: str