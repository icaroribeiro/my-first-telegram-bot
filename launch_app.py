import subprocess

from app.core.logging.logger import get_logger

logger = get_logger()


def main() -> None:
    try:
        logger.info("Starting launching Application...")
        command_args = [
            "uv",
            "run",
            "app/main.py",
        ]
        logger.info(f"Executing command: {' '.join(command_args)}")
        result = subprocess.run(command_args, shell=False, check=False)
        if result.returncode != 0:
            raise Exception(
                f"Application launch failed with return code: {result.returncode}."
            )
        logger.info("Application launch complete.")
    except KeyboardInterrupt:
        message = "Application closed due to KeyboardInterrupt"
        logger.error(message)
    except Exception as error:
        message = f"Error while launching Application: {error}"
        logger.error(message)


if __name__ == "__main__":
    main()
