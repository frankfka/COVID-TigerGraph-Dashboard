import dash_core_components as dcc
import dash_html_components as html
import dash_table

from service.data_provider import app_data_provider


# TODO: Look at last example here: https://dash.plotly.com/datatable/callbacks - need to create lazy loading
def __create_table__(max_rows=100):
    df = app_data_provider.get_patient_info_df()
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=max_rows,
        sort_action='native',
        filter_action='native'
    )


def create_patient_info_tab(props=None):
    """
    Create the view for patient info tab
    :param props:
    :return:
    """
    return __create_table__()
