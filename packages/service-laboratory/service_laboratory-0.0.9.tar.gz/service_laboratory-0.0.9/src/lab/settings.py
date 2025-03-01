import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    database_uri: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/database"
    )
    secret_key: str = Field(default="Secret_Key")
    base_path: str = Field(default=os.path.dirname(os.path.realpath(__file__)))

settings = Settings()
