from dataclasses import dataclass
from typing import Mapping


@dataclass
class PatientTravelledEdge:
    patient_id: str
    travel_event_id: str

    def __hash__(self):
        return hash(self.patient_id + self.travel_event_id)

    @classmethod
    def from_tg_data(cls, data: Mapping):
        return cls(
            patient_id=data["from_id"],
            travel_event_id=data["to_id"]
        )
