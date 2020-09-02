from dataclasses import dataclass
from typing import Mapping


@dataclass
class InfectedByEdge:
    victim_patient_id: str  # Patient being infected
    infector_id: str  # Patient infecting others

    def __hash__(self):
        return hash(self.victim_patient_id + self.infector_id)

    @classmethod
    def from_tg_data(cls, data: Mapping):
        return cls(
            victim_patient_id=data["from_id"],
            infector_id=data["to_id"]
        )
