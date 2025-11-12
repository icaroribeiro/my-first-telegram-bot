from functools import lru_cache
from typing import final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.settings.telegram_settings import get_telegram_settings

telegram_settings = get_telegram_settings()


@final
class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
    )

    api_host: str = Field(default="your_api_host_here")
    api_port: int = Field(default=0)
    api_path_v1: str = Field(default="your_api_path_v1_here")


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()
