import dash_core_components as dcc
import dash_html_components as html

from service.data_provider import app_data_provider


# TODO: Try using DataTable https://dash.plotly.com/datatable
def __create_table__(max_rows=10):
    df = app_data_provider.get_patient_info_df()
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ])


def create_patient_info_tab(props=None):
    """
    Create the view for patient info tab
    :param props:
    :return:
    """
    return __create_table__()