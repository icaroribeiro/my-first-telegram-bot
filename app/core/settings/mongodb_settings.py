from functools import lru_cache
from typing import final

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class MongoDBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MONGODB_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
    )

    driver: str = Field(default="your_driver_here")
    username: str = Field(default="your_username_here")
    password: str = Field(default="your_password_here")
    host: str = Field(default="your_host_here")
    port: int = Field(default=0)
    database: str = Field(default="your_database_here")
    cache_expiration_time_seconds: int = Field(default=0)
    cache_capacity: int = Field(default=0)

    @computed_field
    @property
    def uri(self) -> str:
        return (
            f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}"
        )


@lru_cache
def get_mongodb_settings() -> MongoDBSettings:
    return MongoDBSettings()
