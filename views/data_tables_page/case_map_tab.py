import dash_core_components as dcc
import plotly.express as px
import pandas as pd

from service.data_provider import app_data_provider


def __create_map__() -> dcc.Graph:
    df = app_data_provider.get_cases_df()
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    fig = px.scatter_mapbox(
        df,
        lon='longitude',
        lat='latitude',
        color="confirmed",
        hover_name="case_id",
        size="confirmed", # TODO scale this
        mapbox_style='open-street-map',
        opacity=1,
        zoom=6
    )
    fig.update_layout(
        title='Test Title',
        autosize=True,
        hovermode='closest',
    )
    return dcc.Graph(
        id="case_map",
        figure=fig
    )


def create_case_map_tab(props=None):
    """
    Create the view for case map tab
    :param props:
    :return:
    """
    return __create_map__()
