from dataclasses import dataclass
from typing import Optional, Mapping


@dataclass
class PatientVertex:
    patient_id: str
    infected_by: Optional[str] = None
    symptom_onset_date: Optional[str] = None

    def __hash__(self):
        return hash(self.patient_id)

    @classmethod
    def from_tg_data(cls, data: Mapping):
        data_attributes = data.get('attributes', {})
        return cls(
            patient_id=data["v_id"],  # Must exist
            infected_by=data_attributes.get("infected_by", None),
            symptom_onset_date=data_attributes.get("symptom_onset_date", None)
        )