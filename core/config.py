from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Settings

    All aplication settings to controll
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Run configs
    DEBUG: bool
    HOST: str
    PORT: int
    RELOAD: bool  # Remove this if you deploy

    # Database config
    DATABASE_URL: str

    # Database for tests
    DATABASE_URL_TEST: str

    # JWT config
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS config
    ALLOWED_ORIGINS: list[str] = ["*"]


@lru_cache
def get_settings():
    return Settings()
