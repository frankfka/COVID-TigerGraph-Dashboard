from .home_page.layout import layout as home_page_layout
from .data_tables_page.layout import layout as data_tables_page_layout
from .graph_page.layout import layout as graph_page_layout
from .routes import *

# All Pages
pages = {
    HOME_ROUTE: home_page_layout,
    DATA_TABLES_ROUTE: data_tables_page_layout,
    GRAPH_ROUTE: graph_page_layout
}