from pydantic import BaseSettings

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


class CommonSettings(BaseSettings):
    PROJECT_NAME: str = "todolist2"
    APP_NAME: str = "todolist App"
    DEBUG_MODE: bool = config("DEBUG_MODE", cast=bool)
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    SECRET_KEY: str = config("SECRET_KEY", cast=Secret, default="CHANGEME")


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    MONGODB_URL: str = config("MONGODB_URL", cast=str)
    MONGODB_NAME: str = config("MONGODB_NAME", cast=str)

    POSTGRES_USER: str = config("POSTGRES_USER", cast=str)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=Secret, default="CHANGEME")
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", cast=str, default="db")
    POSTGRES_PORT: str = config("POSTGRES_PORT", cast=str, default="5432")
    POSTGRES_DB: str = config("POSTGRES_DB", cast=str)
    DATABASE_URL: str = config(
        "DATABASE_URL",
        cast=str,
        default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    DATABASE_TODO_TABLE = config("DATABASE_TODO_TABLE", cast=str)


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
