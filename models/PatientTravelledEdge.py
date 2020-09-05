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
        # Bidirectional edge, so need to get types:
        if data['from_type'] == "TravelEvent":
            patient_id = data["to_id"]
            travel_event_id = data["from_id"]
        else:
            patient_id = data["from_id"]
            travel_event_id = data["to_id"]
        return cls(
            patient_id=patient_id,
            travel_event_id=travel_event_id
        )
