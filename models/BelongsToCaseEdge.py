from dataclasses import dataclass
from typing import Mapping


@dataclass
class BelongsToCaseEdge:
    patient_id: str
    infection_case_id: str

    def __hash__(self):
        return hash(self.patient_id + self.infection_case_id)

    @classmethod
    def from_tg_data(cls, data: Mapping):
        return cls(
            patient_id=data["from_id"],
            infection_case_id=data["to_id"]
        )
