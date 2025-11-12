from fastapi import FastAPI

from app.app_wrapper import AppWrapper
from app.core.logging.logger import get_logger

logger = get_logger()

inner_app: FastAPI | None = None

try:
    app_wrapper: AppWrapper = AppWrapper()
    inner_app = app_wrapper.app
except Exception as error:
    message = f"Error while starting Application: {error}"
    logger.error(message)
    raise Exception(message)
