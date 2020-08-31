from typing import List, Dict

import pandas as pd

from config import Config, app_config
from models.InfectedByEdge import InfectedByEdge
from models.InfectionCaseVertex import InfectionCaseVertex
from models.PatientVertex import PatientVertex
from util import get_path

from service.tigergraph_service import TigerGraphService


class DataProvider:
    """
    Responsible for retrieval & update of all data for views
    """

    def __init__(self, config: Config):
        self.db = TigerGraphService(config)
        return

    def get_infection_case_vertices(self) -> List[InfectionCaseVertex]:
        vertices = self.db.get_infection_case_vertices(limit=50, sort_by_attrs=["id"])
        return [
            InfectionCaseVertex.from_tg_data(vertex)
            for vertex in vertices
        ]

    def get_patient_vertices(self) -> List[PatientVertex]:
        vertices = self.db.get_patient_vertices(limit=50, sort_by_attrs=["patient_id"])
        return [
            PatientVertex.from_tg_data(vertex)
            for vertex in vertices
        ]

    def get_infected_by_edges(self, source_patients: List[PatientVertex]) -> List[Dict]:
        edges = self.db.get_infected_by_edges(
            source_ids=[patient.patient_id for patient in source_patients],
            limit=50
        )
        return [
            InfectedByEdge.from_tg_data(edge)
            for edge in edges
        ]

    def get_patient_info_df(self) -> pd.DataFrame:
        # TODO: Caching
        return pd.read_csv(get_path('data/PatientInfo.csv'))

    def get_cases_df(self) -> pd.DataFrame:
        return pd.read_csv(get_path('data/Case.csv'))


# Instance of DataProvider that should be used in all views
app_data_provider = DataProvider(app_config)
