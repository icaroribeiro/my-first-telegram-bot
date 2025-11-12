from fastapi import status

from app.app_error import AppError
from app.core.logging.logger import get_logger
from app.infrastructure.mongodb.mongodb import MongoDB

logger = get_logger()


class HealthCheckService:
    def __init__(self, mongodb: MongoDB) -> None:
        self.mongodb = mongodb

    async def check_health(self) -> None:
        logger.info("Starting checking Health...")
        try:
            await self.mongodb.client.admin.command("ping")
            logger.info("Health checked successully.")
        except Exception as error:
            message = f"Error while checking health: {error}"
            logger.error(message)
            return AppError(
                message=message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )
