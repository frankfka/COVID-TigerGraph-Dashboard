from dataclasses import dataclass
from typing import Mapping


@dataclass
class InfectionCaseVertex:
    case_id: str
    num_confirmed_cases: int

    def __hash__(self):
        return hash(self.case_id)

    @classmethod
    def from_tg_data(cls, data: Mapping):
        attributes = data.get("attributes", {})
        return cls(
            case_id=data["v_id"],
            num_confirmed_cases=attributes.get("confirmed", 0)
        )
