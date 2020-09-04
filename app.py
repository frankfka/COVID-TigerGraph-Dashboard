import dash
from flask_caching import Cache

from config import app_config

main_app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = main_app.server

main_app_cache = Cache(server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': app_config.app_cache_dir
})
