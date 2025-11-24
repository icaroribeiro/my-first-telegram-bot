from typing import Type

from pymongo import AsyncMongoClient

from app.core.logging.logger import get_logger
from app.core.settings.mongodb_settings import MongoDBSettings
from beanie import Document, init_beanie

logger = get_logger()


class MongoDB:
    def __init__(
        self,
        mongodb_settings: MongoDBSettings,
    ) -> None:
        self.mongodb_settings = mongodb_settings
        self.client: AsyncMongoClient = self._create_client()

    async def init_database(self, document_models: list[Type[Document]]) -> None:
        try:
            logger.info("Starting initializing Beanie with documents...")
            database = self.client[self.mongodb_settings.database]
            await init_beanie(database, document_models=document_models)
            logger.info("Beanie with documents initialized")
        except Exception as error:
            message = f"Error while initializing Beanie: {error}"
            logger.error(message)
            raise Exception(message)

    async def check_collection_existence(
        self,
        document_model: Type[Document],
    ) -> bool:
        collection_name: str = ""
        try:
            collection_name = document_model.Settings.name
            logger.info(
                f"Starting checking collection '{collection_name}' existence..."
            )
            database = self.client[self.mongodb_settings.database]
            existing_collection_names = await database.list_collection_names()
            if collection_name in existing_collection_names:
                logger.info(f"Collection '{collection_name}' exists.")
                return True
            logger.info(f"Collection '{collection_name}' doesn't exist.")
            return False
        except Exception as error:
            message = f"Error while checking collection '{collection_name}' existence: {error}"
            logger.error(message)
            raise Exception(message)

    async def create_collection(
        self,
        document_model: Type[Document],
    ) -> bool:
        collection_name: str = ""
        try:
            logger.info(f"Starting creating collection '{collection_name}'...")
            collection_name = document_model.Settings.name
            database = self.client[self.mongodb_settings.database]
            await database.create_collection(collection_name)
            logger.info(f"Collection '{collection_name}' created.")
        except Exception as error:
            logger.warning(
                f"Error while creating collection '{collection_name}': {error}"
            )

    async def close(self):
        try:
            logger.info("Starting closing MongoDB client...")
            await self.client.close()
            logger.info("MongoDB client closed.")
        except Exception as error:
            message = f"Error while closing MongoDB client: {error}"
            logger.error(message)
            raise Exception(message)

    def _create_client(self) -> AsyncMongoClient:
        try:
            logger.info("Starting creating MongoDB client pool...")
            client = AsyncMongoClient(self.mongodb_settings.uri)
            logger.info("MongoDB client pool created.")
            return client
        except Exception as error:
            message = f"Error while creating MongoDB client pool: {error}"
            logger.error(message)
            raise Exception(message)
