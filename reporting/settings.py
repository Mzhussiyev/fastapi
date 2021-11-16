from pydantic import BaseSettings

class AppConfig(BaseSettings):
    db_url: str

def get_config() -> AppConfig:
    return AppConfig()