import os
from dataclasses import dataclass

from util import load_env

load_env()


@dataclass
class Config:
    tg_username: str
    tg_password: str
    tg_api_key: str

    def __init__(self):
        # Inject environment variables from local file
        load_env()
        self.tg_username = os.getenv("TG_USERNAME")
        self.tg_password = os.getenv("TG_PASSWORD")
        self.tg_api_key = os.getenv("TG_API_KEY")


# Singleton configuration instance
app_config = Config()
