from pydantic import Field
from pymongo.asynchronous.client_session import AsyncClientSession

from app.core.logging.logger import get_logger
from app.infrastructure.mongodb.documents.ui_translation_document import (
    Languages,
    UITranslationBaseDocument,
    UITranslationKey,
)
from beanie import free_fall_migration

logger = get_logger()


class OldUITranslationDocument(UITranslationBaseDocument):
    pass


class NewUITranslationDocument(UITranslationBaseDocument):
    key: str = Field(description="Key to identify the string texts.")
    text: Languages = Field(
        description="String texts translated into various languages."
    )


class Forward:
    @free_fall_migration(document_models=[NewUITranslationDocument])
    async def upgrade(self, session: AsyncClientSession | None = None):
        collection_name: str = ""
        try:
            collection_name = UITranslationBaseDocument.Settings.name
            logger.info(f"Starting seeding new data in collection {collection_name}...")
            ui_translation_data = [
                NewUITranslationDocument(
                    key=UITranslationKey.COMMAND_DESC_START.value,
                    text=Languages(
                        pt="Iniciar o diálogo principal do bot",
                        en="Start the main bot dialog",
                    ),
                ),
            ]
            await NewUITranslationDocument.insert_many(
                documents=ui_translation_data, session=session
            )
            logger.info(f"All documents from collection '{collection_name}' inserted.")
        except Exception as error:
            message = f"Error while seeding initial data in collection '{collection_name}': {error}"
            logger.error(message)
            raise Exception(message)


class Backward:
    @free_fall_migration(document_models=[NewUITranslationDocument])
    async def downgrade(self, session: AsyncClientSession | None = None):
        collection_name: str = ""
        try:
            collection_name = UITranslationBaseDocument.Settings.name
            logger.info(
                f"Starting deleting documents from collection '{collection_name}'..."
            )
            keys_to_delete = [
                UITranslationKey.COMMAND_DESC_START.value,
            ]
            await NewUITranslationDocument.delete_many(
                {"key": {"$in": keys_to_delete}},
                session=session,
            )
            logger.info(f"All documents from collection '{collection_name}' deleted.")
        except Exception as error:
            message = f"Error while deleting documents from collection '{collection_name}': {error}"
            logger.error(message)
            raise Exception(message)
