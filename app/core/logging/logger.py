import logging
from functools import lru_cache


class Logger:
    def __init__(self) -> None:
        self.__logger = self.__create_logger()

    @property
    def logger(self) -> logging.Logger:
        if self.__logger is None:
            self.__logger = self.__create_logger()
        return self.__logger

    @staticmethod
    def __create_logger() -> logging.Logger:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        # handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        # if not logger.hasHandlers():
        #     logger.addHandler(handler)
        return logger


@lru_cache
def get_logger() -> logging.Logger:
    return Logger().logger
