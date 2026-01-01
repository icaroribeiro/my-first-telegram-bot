import uvicorn

from app.core.logging.logger import get_logger
from app.core.settings.app_settings import get_app_settings

logger = get_logger()
app_settings = get_app_settings()

logger = get_logger()


def main() -> None:
    try:
        logger.info("Starting initiating Uvicorn ..")
        uvicorn.run(
            app="app:inner_app",
            host=app_settings.api_host,
            port=int(app_settings.api_port),
            reload=True,
        )
    except KeyboardInterrupt:
        message = "Application closed due to KeyboardInterrupt"
        logger.error(message)
    except Exception as error:
        message = f"Error while initiating Uvicorn server: {error}"
        logger.error(message)
        raise Exception(message)


if __name__ == "__main__":
    main()
