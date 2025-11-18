from functools import lru_cache
from typing import final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class TaskQueueSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TASK_QUEUE_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
    )

    num_workers: int = Field(default=0)
    queue_max_size: int = Field(default=0)
    max_retries: int = Field(default=0)
    initial_backoff_seconds: int = Field(default=0)
    async_task_timeout_seconds: int = Field(default=0)


@lru_cache
def get_task_queue_settings() -> TaskQueueSettings:
    return TaskQueueSettings()
