from dataclasses import dataclass
from typing import Optional, Mapping


@dataclass
class TravelEventVertex:
    event_id: str
    latitude: float = None
    longitude: float = None
    visited_date: str = None
    travel_type: str = None

    def __hash__(self):
        return hash(self.event_id)

    @classmethod
    def from_tg_data(cls, data: Mapping):
        data_attributes = data.get('attributes', {})
        return cls(
            event_id=data["v_id"],  # Must exist
            latitude=data_attributes.get("latitude"),
            longitude=data_attributes.get("longitude"),
            visited_date=data_attributes.get("visited_date"),
            travel_type=data_attributes.get("travel_type")
        )