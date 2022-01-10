from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Awesome API"
    TESTING: bool = False
    DB_URL: str
    DB_TEST_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
