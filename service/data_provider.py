from typing import List, Dict

import pandas as pd

from config import Config, app_config
from models.BelongsToCaseEdge import BelongsToCaseEdge
from models.InfectedByEdge import InfectedByEdge
from models.InfectionCaseVertex import InfectionCaseVertex
from models.PatientTravelledEdge import PatientTravelledEdge
from models.PatientVertex import PatientVertex
from models.TravelEventVertex import TravelEventVertex
from util import get_path

from service.tigergraph_service import TigerGraphService


class DataProvider:
    """
    Responsible for retrieval & update of all data for views
    """

    def __init__(self, config: Config):
        self.db = TigerGraphService(config)
        return

    def get_patient_vertices(self) -> List[PatientVertex]:
        vertices = self.db.get_patient_vertices(sort_by_attrs=["patient_id"])
        return [
            PatientVertex.from_tg_data(vertex)
            for vertex in vertices
        ]

    def get_infected_by_edges(self, patients: List[PatientVertex]) -> List[InfectedByEdge]:
        patient_ids = [patient.patient_id for patient in patients]
        edges = self.db.get_infected_by_edges(from_patient_ids=patient_ids)
        # Can't have a target if the target_id is not in the set of patient ID's that we retrieve
        infected_by_edges: List[InfectedByEdge] = []
        for edge in edges:
            parsed_edge = InfectedByEdge.from_tg_data(edge)
            if parsed_edge.infector_id in patient_ids:
                infected_by_edges.append(parsed_edge)
        return infected_by_edges

    def expand_infection_case_vertices(
            self, patient_vertices: List[PatientVertex]
    ) -> (List[BelongsToCaseEdge], List[InfectionCaseVertex]):
        patient_ids = [p.patient_id for p in patient_vertices]
        outgoing_edges = [
            BelongsToCaseEdge.from_tg_data(edge) for edge in
            self.db.get_belongs_to_case_edges(from_patient_ids=patient_ids)
        ]
        infection_case_ids = [e.infection_case_id for e in outgoing_edges]
        infection_vertices = [
            InfectionCaseVertex.from_tg_data(vertex) for vertex in
            self.db.get_infection_case_vertices_by_id(infection_case_ids)
        ]
        return outgoing_edges, infection_vertices

    def expand_travel_event_vertices(
            self, patient_vertices: List[PatientVertex]
    ) -> (List[PatientTravelledEdge], List[TravelEventVertex]):
        patient_ids = [p.patient_id for p in patient_vertices]
        outgoing_edges = [
            PatientTravelledEdge.from_tg_data(edge) for edge in
            self.db.get_patient_travelled_edges(from_patient_ids=patient_ids)
        ]
        travel_event_ids = [e.travel_event_id for e in outgoing_edges]
        travel_event_vertices = [
            TravelEventVertex.from_tg_data(vertex) for vertex in
            self.db.get_travel_event_vertices_by_id(travel_event_ids)
        ]
        return outgoing_edges, travel_event_vertices


    """
    Static Data
    """

    def get_patient_info_df(self) -> pd.DataFrame:
        # TODO: Caching
        return pd.read_csv(get_path('data/PatientInfo.csv'))

    def get_cases_df(self) -> pd.DataFrame:
        return pd.read_csv(get_path('data/Case.csv'))


# Instance of DataProvider that should be used in all views
app_data_provider: DataProvider = DataProvider(app_config)
