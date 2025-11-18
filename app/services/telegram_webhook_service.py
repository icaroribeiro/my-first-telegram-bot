from typing import Any

from aiogram import Bot, Dispatcher

# You must import this:
from aiogram.methods import TelegramMethod
from aiogram.types import Update
from fastapi import status

from app.app_error import AppError
from app.core.logging.logger import get_logger

logger = get_logger()


class TelegramWebhookService:
    @staticmethod
    async def handle_webhook(
        json_data: dict[str, Any], dispatcher: Dispatcher, bot: Bot
    ) -> bool:
        try:
            update = Update(**json_data)
            result = await dispatcher.feed_update(bot=bot, update=update)
            if isinstance(result, TelegramMethod):
                await dispatcher.silent_call_request(bot=bot, result=result)
            return True
        except Exception as error:
            message = f"Error while feeding update to dispatcher: {error}"
            logger.error(message, exc_info=True)
            return False

    @staticmethod
    async def on_webhook_startup(
        bot: Bot, webhook_url: str, webhook_secret: str
    ) -> None:
        try:
            logger.info("Starting initiating webhook startup...")
            webhook_info = await bot.get_webhook_info()
            if webhook_info.url != webhook_url:
                await bot.set_webhook(url=webhook_url, secret_token=webhook_secret)
            logger.info(
                f"Webhook started successully for bot {bot.id} at {webhook_url}."
            )
        except Exception as error:
            message = f"Error while starting up webhook for bot {bot.id} at {webhook_url}: {error}"
            logger.error(message)
            raise AppError(
                message=message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )

    @staticmethod
    async def on_webhook_shutdown(
        bot: Bot,
        webhook_url: str,
    ) -> None:
        try:
            logger.info("Starting initiating webhook shut down...")
            if await bot.delete_webhook():
                logger.info("Bot webhook dropped.")
            else:
                logger.error("Failed to drop bot webhook.")
            await bot.session.close()
            logger.info(
                f"Webhook shut down successully for bot {bot.id} at {webhook_url}."
            )
        except Exception as error:
            message = f"Error while shutting down webhook for bot {bot.id} at {webhook_url}: {error}"
            logger.error(message)
            raise AppError(
                message=message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )
