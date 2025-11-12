from enum import Enum
from functools import lru_cache
from typing import final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class UpdateMethod(str, Enum):
    WEBHOOK = "webhook"
    POLLING = "polling"


@final
class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TELEGRAM_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
    )

    mode: UpdateMethod = Field(default="your_mode_here")
    base_webhook_url: str = Field(default="your_base_webhook_url_here")
    webhook_path_v1: str = Field(default="your_webhook_path_v1_here")
    bot_token_v1: str = Field(default="your_bot_token_1_here")
    webhook_secret_v1: str = Field(default="your_webhook_secret_v1_here")


@lru_cache
def get_telegram_settings() -> TelegramSettings:
    return TelegramSettings()
