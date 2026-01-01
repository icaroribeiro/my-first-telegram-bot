from enum import Enum

from pydantic import BaseModel, Field
from pymongo import ASCENDING, IndexModel

from app.infrastructure.mongodb.documents.base_document import BaseDocument


class UITranslationKey(str, Enum):
    COMMAND_DESC_START = "command_desc_start"


class Languages(BaseModel):
    pt: str = Field(description="String text translated into Portuguese.")
    en: str = Field(description="String text translated into English.")


class UITranslationBaseDocument(BaseDocument):
    class Settings:
        name = "ui_translation"
        IndexModel([("key", ASCENDING)], unique=True)


class UITranslationDocument(UITranslationBaseDocument):
    key: str = Field(description="Key to identify the string texts.")
    text: Languages = Field(
        description="String texts translated into various languages."
    )
