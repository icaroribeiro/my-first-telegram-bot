import asyncio
import os
import subprocess

from app.core.logging.logger import get_logger
from app.core.settings.mongodb_settings import get_mongodb_settings
from app.infrastructure.mongodb.mongodb import MongoDB

logger = get_logger()
mongodb_settings = get_mongodb_settings()


async def main() -> None:
    mongodb = MongoDB(mongodb_settings=mongodb_settings)

    try:
        logger.info("Starting establishing MongoDB connection...")
        await mongodb.client.admin.command("ping")
        logger.info("MongoDB connection establishment complete.")
    except Exception as error:
        message = f"Error while establishing MongoDB connection: {error}"
        logger.error(message)
        raise Exception(message)

    try:
        logger.info("Starting migrating Beanie...")
        migration_path = os.path.join(os.getcwd(), "beanie", "migrations")
        command_args = [
            "beanie",
            "migrate",
            "-uri",
            mongodb_settings.uri,
            "-db",
            mongodb_settings.database,
            "-p",
            migration_path,
            "--no-use-transaction",
        ]
        logger.info(f"Executing command: {' '.join(command_args)}")
        result = subprocess.run(command_args, shell=False, check=False)
        if result.returncode != 0:
            raise Exception(
                f"Beanie migration failed with return code: {result.returncode}."
            )
        logger.info("Beanie migration complete.")
    except Exception as error:
        message = f"Error while migrating Beanie: {error}"
        logger.error(message)
        raise Exception(message)

    try:
        logger.info("Starting closing MongoDB connections...")
        await mongodb.close()
        logger.info("MongoDB connections closure complete.")
    except Exception as error:
        message = f"Error while closing MongoDB connections: {error}"
        logger.error(message)
        raise Exception(message)


if __name__ == "__main__":
    asyncio.run(main())
