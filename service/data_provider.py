import pandas as pd

from paths import get_path


class DataProvider:
    """
    Responsible for retrieval & update of all data for views
    """

    def __init__(self):
        pass

    def get_patient_info_df(self) -> pd.DataFrame:
        # TODO: Caching
        return pd.read_csv(get_path('data/PatientInfo.csv'))

    def get_cases_df(self) -> pd.DataFrame:
        return pd.read_csv(get_path('data/Case.csv'))


# Instance of DataProvider that should be used in all views
app_data_provider = DataProvider()
