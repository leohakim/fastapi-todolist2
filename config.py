from pydantic import BaseSettings
import os

class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Starter"
    DEBUG_MODE: bool = os.getenv('DB_URL', False)


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = os.getenv('DB_URL')
    DB_NAME: str = os.getenv('DB_NAME')


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
