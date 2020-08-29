from typing import List, Dict

import pandas as pd

from paths import get_path

# TODO: Data classes
class DataProvider:
    """
    Responsible for retrieval & update of all data for views
    """

    def __init__(self):
        pass

    def get_patient_vertices(self) -> List[Dict]:
        return [
            {
                "patient_id": patient_row["patient_id"],
                "symptom_onset_date": patient_row["symptom_onset_date"]
            } for _, patient_row in self.get_patient_info_df().iterrows()
        ]

    def get_infected_by_edges(self) -> List[Dict]:
        # Some "infected_by" items are not actual patients in the CSV, so need to filter those out
        available_patient_ids = set([
            patient_row["patient_id"] for _, patient_row in self.get_patient_info_df().iterrows()
        ])
        return [
            {
                "source": patient_row["patient_id"],
                "target": patient_row["infected_by"]
            } for _, patient_row in self.get_patient_info_df().iterrows()
            if patient_row["infected_by"] and patient_row["infected_by"] in available_patient_ids
        ]

    def get_patient_info_df(self) -> pd.DataFrame:
        # TODO: Caching
        return pd.read_csv(get_path('data/PatientInfo.csv')).head(100)

    def get_cases_df(self) -> pd.DataFrame:
        return pd.read_csv(get_path('data/Case.csv'))


# Instance of DataProvider that should be used in all views
app_data_provider = DataProvider()
