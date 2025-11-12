from datetime import datetime, timedelta, timezone

from bson import ObjectId
from pydantic import Field

from app.core.settings.mongodb_settings import MongoDBSettings
from beanie import Document, PydanticObjectId


class BaseDocument(Document):
    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")
    created_at: datetime = Field(
        default=datetime.now(tz=timezone.utc), alias="data_criacao"
    )
    updated_at: datetime = Field(
        default=datetime.now(tz=timezone.utc), alias="data_atualizacao"
    )

    async def pre_save(self):
        self.updated_at = datetime.now(tz=timezone.utc)
        return await self.save()

    class Settings:
        use_state_management = True
        validate_on_save = True
        use_cache = True
        cache_expiration_time = timedelta(
            seconds=MongoDBSettings().cache_expiration_time_seconds
        )
        cache_capacity = MongoDBSettings().cache_capacity
