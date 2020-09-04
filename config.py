import os
from dataclasses import dataclass

from util import load_env, get_path

load_env()


@dataclass
class Config:
    """Holds application configuration"""

    # App Caching
    app_cache_dir: str
    app_cache_default_timeout: float

    # TigerGraph
    tg_host: str
    tg_graph: str
    tg_username: str
    tg_password: str
    tg_api_key: str

    def __init__(self):
        # Inject environment variables from local file
        load_env()
        self.app_cache_dir = get_path("cache/app_cache").absolute().__str__()
        self.app_cache_default_timeout = 60
        self.tg_host = os.getenv("TG_HOST")
        self.tg_graph = os.getenv("TG_GRAPH")
        self.tg_username = os.getenv("TG_USERNAME")
        self.tg_password = os.getenv("TG_PASSWORD")
        self.tg_api_key = os.getenv("TG_API_KEY")


# Singleton configuration instance
app_config = Config()
