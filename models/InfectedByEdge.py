from dataclasses import dataclass
from typing import Optional, Mapping


@dataclass
class InfectedByEdge:
    source_id: str
    target_id: str

    def __hash__(self):
        return hash(self.source_id + self.target_id)

    @classmethod
    def from_tg_data(cls, data: Mapping):
        return cls(
            source_id=data["from_id"],
            target_id=data["to_id"]
        )
