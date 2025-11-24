from pymongo.asynchronous.client_session import AsyncClientSession

from app.core.logging.logger import get_logger
from app.infrastructure.mongodb.documents.bmi_category_document import (
    BMICategoryBaseDocument,
)
from beanie import free_fall_migration

logger = get_logger()


class Forward:
    @free_fall_migration(document_models=[BMICategoryBaseDocument])
    async def upgrade(self, session: AsyncClientSession | None = None):
        collection_name: str = ""
        try:
            collection_name = BMICategoryBaseDocument.Settings.name
            logger.info(
                f"Starting checking collection '{collection_name}' existence..."
            )
            async_collection = BMICategoryBaseDocument.get_pymongo_collection()
            database = async_collection.database
            existing_collection_names = await database.list_collection_names()
            if collection_name in existing_collection_names:
                logger.info(
                    f"Collection '{collection_name}' already exists. Skipping creation."
                )
                return
            logger.info(f"Collection '{collection_name}' doesn't exist.")
        except Exception as error:
            message = f"Error while checking collection '{collection_name}' existence: {error}"
            logger.error(message)
            raise Exception(message)

        try:
            logger.info(f"Starting creating collection '{collection_name}'...")
            await database.create_collection(name=collection_name, session=session)
            logger.info(f"Collection '{collection_name}' created.")
        except Exception as error:
            logger.warning(
                f"Error while creating collection '{collection_name}': {error}"
            )


class Backward:
    @free_fall_migration(document_models=[BMICategoryBaseDocument])
    async def downgrade(self, session: AsyncClientSession | None = None):
        collection_name: str = ""
        try:
            collection_name = BMICategoryBaseDocument.Settings.name
            logger.info(
                f"Starting checking collection '{collection_name}' existence..."
            )
            async_collection = BMICategoryBaseDocument.get_pymongo_collection()
            database = async_collection.database
            existing_collection_names = await database.list_collection_names()
            if collection_name not in existing_collection_names:
                logger.info(
                    f"Collection '{collection_name}' doesn't exist. Skipping drop."
                )
                return
        except Exception as error:
            message = f"Error while checking collection '{collection_name}' existence: {error}"
            logger.error(message)
            raise Exception(message)

        try:
            logger.info(f"Starting dropping collection '{collection_name}'...")
            await database.drop_collection(
                name_or_collection=collection_name, session=session
            )
            logger.info(f"Collection '{collection_name}' dropped.")
        except Exception as error:
            logger.warning(
                f"Error while dropping collection '{collection_name}': {error}"
            )
