from pydantic import Field

from app.infrastructure.mongodb.documents.ui_translation_document import (
    Languages,
    UITranslationBaseDocument,
)
from beanie import iterative_migration


class OldUITranslationDocument(UITranslationBaseDocument):
    pass


class NewUITranslationDocument(UITranslationBaseDocument):
    key: str = Field(description="Key to identify the string texts.")
    text: Languages = Field(
        description="String texts translated into various languages."
    )


class Forward:
    @iterative_migration()
    async def upgrade(
        self,
        input_document: OldUITranslationDocument,
        output_document: NewUITranslationDocument,
    ):
        pass


class Backward:
    @iterative_migration()
    async def downgrade(
        self,
        input_document: OldUITranslationDocument,
        output_document: NewUITranslationDocument,
    ):
        pass
