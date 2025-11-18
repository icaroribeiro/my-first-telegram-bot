from pymongo import AsyncMongoClient

from app.core.logging.logger import get_logger
from app.core.settings.mongodb_settings import MongoDBSettings

logger = get_logger()


class MongoDB:
    def __init__(
        self,
        mongodb_settings: MongoDBSettings,
    ) -> None:
        self.mongodb_settings = mongodb_settings
        self.client: AsyncMongoClient = self.__create_client()

    async def close(self):
        try:
            logger.info("Starting closing MongoDB client...")
            await self.client.close()
            logger.info("MongoDB client closed successfully.")
        except Exception as error:
            message = f"Error while closing MongoDB client: {error}"
            logger.error(message)
            raise Exception(message)

    def __create_client(self) -> AsyncMongoClient:
        try:
            logger.info("Starting creating MongoDB client pool...")
            client = AsyncMongoClient(self.mongodb_settings.uri)
            logger.info("MongoDB client pool created successfully.")
            return client
        except Exception as error:
            message = f"Error while creating MongoDB client pool: {error}"
            logger.error(message)
            raise Exception(message)
