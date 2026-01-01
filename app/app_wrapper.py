import functools
from asyncio import create_task

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.pymongo import PyMongoStorage
from aiogram.types import LinkPreviewOptions
from aiogram_dialog import (
    setup_dialogs,
)
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.api.common.handlers.exception_handler import (
    ExceptionHandler,
)
from app.api.common.middlewares.logging_middleware import (
    LoggingMiddleware,
)
from app.api.common.routers.healthcheck_router import (
    api_router as healthcheck_router_v1,
)
from app.api.v1.routers.telegram_webhook_router import (
    api_router as telegram_webhook_router_v1,
)
from app.app_error import AppError
from app.bots.v1.commands.set_default_commands import set_default_commands
from app.bots.v1.dialogs.bmi_dialog import (
    bmi_dialog as bmi_dialog_v1,
)
from app.bots.v1.handlers.exit_handler import (
    exit_handler as exit_handler_v1,
)
from app.bots.v1.handlers.help_handler import help_handler as help_handler_v1
from app.bots.v1.handlers.start_handler import (
    start_handler as start_handler_v1,
)
from app.bots.v1.handlers.unknown_intent_handler import (
    unknown_intent_handler as unknown_intent_handler_v1,
)
from app.bots.v1.handlers.unknown_state_handler import (
    unknown_state_handler as unknown_state_handler_v1,
)
from app.core.container.container import Container
from app.core.logging.logger import get_logger
from app.core.settings.app_settings import get_app_settings
from app.core.settings.mongodb_settings import get_mongodb_settings
from app.core.settings.telegram_settings import UpdateMethod, get_telegram_settings
from app.infrastructure.mongodb.documents import get_documments
from app.infrastructure.mongodb.mongodb import MongoDB
from app.infrastructure.task_queue.task_queue_consumer import TaskQueueConsumer
from app.services.telegram_webhook_service import TelegramWebhookService

logger = get_logger()
app_settings = get_app_settings()
mongodb_settings = get_mongodb_settings()
telegram_settings = get_telegram_settings()


class AppWrapper:
    _app: FastAPI | None = None
    _mongodb: MongoDB | None = None
    _task_queue_consumer: TaskQueueConsumer | None = None
    _telegram_webhook_service: TelegramWebhookService | None = None

    _bot_v1: Bot | None = None
    _dispatcher_v1: Dispatcher | None = None

    def __init__(self) -> None:
        self._container: Container = Container()
        self._mongodb: MongoDB = self._container.mongodb()
        self._task_queue_consumer: TaskQueueConsumer = (
            self._container.task_queue_consumer()
        )
        self._telegram_webhook_service: TelegramWebhookService = (
            self._container.telegram_webhook_service()
        )
        self._container.wire(
            modules=[
                "app.bots.v1.handlers.weight_change_handler",
            ],
            packages=[
                "app.api.v1.routers",
            ],
        )
        self._app = FastAPI(
            title="My First Telegram Bot API",
            description="A REST API developed using Python, FastAPI framework and MongoDB."
            + "Some useful links:\n\n"
            + "[My First Telegram Bot API repository](https://github.com/icaroribeiro/my-first-telegram-bot)\n\n",  # noqa: E501
            version="1.0.0",
            contact={
                "name": "Ícaro Ribeiro",
                "email": "icaroribeiro@hotmail.com",
                "url": "https://github.com/icaroribeiro",
            },
            license_info={
                "name": "MIT",
            },
            openapi_tags=[
                {
                    "name": "v1",
                    "description": "V1 API endpoints",
                }
            ],
            servers=[
                {
                    "url": "http://localhost:8000",
                    "description": "Homologation environment",
                },
                {
                    "url": "http://localhost:8000",
                    "description": "Production environment",
                },
            ],
        )
        if telegram_settings.mode == UpdateMethod.WEBHOOK.value:
            self._setup_telegram_webhook_router_v1()
        elif telegram_settings.mode == UpdateMethod.POLLING.value:
            self._setup_telegram_polling_v1()
        else:
            raise Exception(
                "Error while checking telegram update method: "
                + "Update method not recognized."
            )
        self._setup_api_router_v1()
        self._setup_api_middlewares()
        self._setup_api_exception_handlers()
        self._setup_api_event_handlers()

    def _setup_telegram_webhook_router_v1(self) -> None:
        self._bot_v1: Bot = Bot(
            token=telegram_settings.bot_token_v1,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
                link_preview=LinkPreviewOptions(is_disabled=True),
            ),
        )
        storage_v1 = PyMongoStorage(
            client=self._mongodb.client,
            db_name=mongodb_settings.database,
            collection_name="states_and_data_v1",
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
        self._dispatcher_v1: Dispatcher = Dispatcher(storage=storage_v1)
        self._dispatcher_v1.startup.register(
            functools.partial(
                self._telegram_webhook_service.on_webhook_startup,
                webhook_url=f"{telegram_settings.base_webhook_url}/"
                + f"{app_settings.api_path_v1}/"
                + f"{telegram_settings.webhook_path_v1}/"
                + f"{telegram_settings.bot_token_v1}",
                webhook_secret=telegram_settings.webhook_secret_v1,
            )
        )
        self._dispatcher_v1.startup.register(set_default_commands)
        self._dispatcher_v1.message.register(start_handler_v1, CommandStart())
        self._dispatcher_v1.message.register(help_handler_v1, Command("help"))
        self._dispatcher_v1.message.register(exit_handler_v1, Command("exit"))
        self._dispatcher_v1.errors.register(
            unknown_intent_handler_v1,
            ExceptionTypeFilter(UnknownIntent),
        )
        self._dispatcher_v1.errors.register(
            unknown_state_handler_v1,
            ExceptionTypeFilter(UnknownState),
        )
        self._dispatcher_v1.include_router(router=bmi_dialog_v1)
        setup_dialogs(router=self._dispatcher_v1)
        self._app.state.bot_v1 = self._bot_v1
        self._app.state.dispatcher_v1 = self._dispatcher_v1

    def _setup_telegram_polling_v1(self) -> None:
        self._bot_v1: Bot = Bot(
            token=telegram_settings.bot_token_v1,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
                link_preview=LinkPreviewOptions(is_disabled=True),
            ),
        )
        storage_v1 = PyMongoStorage(
            client=self._mongodb.client,
            db_name=mongodb_settings.database,
            collection_name="states_and_data_v1",
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
        self._dispatcher_v1: Dispatcher = Dispatcher(storage=storage_v1)
        self._dispatcher_v1.startup.register(set_default_commands)
        self._dispatcher_v1.message.register(start_handler_v1, CommandStart())
        self._dispatcher_v1.message.register(help_handler_v1, Command("help"))
        self._dispatcher_v1.message.register(exit_handler_v1, Command("exit"))
        self._dispatcher_v1.errors.register(
            unknown_intent_handler_v1, ExceptionTypeFilter(UnknownIntent)
        )
        self._dispatcher_v1.errors.register(
            unknown_state_handler_v1, ExceptionTypeFilter(UnknownState)
        )
        self._dispatcher_v1.include_router(router=bmi_dialog_v1)
        setup_dialogs(router=self._dispatcher_v1)
        self._app.state.bot_v1 = self._bot_v1
        self._app.state.dispatcher_v1 = self._dispatcher_v1

    @staticmethod
    async def on_dispatcher_startup(
        dispatcher: Dispatcher | None = None, bot: Bot | None = None
    ) -> None:
        if dispatcher and bot:
            await dispatcher.emit_startup(bot=bot, **dispatcher.workflow_data)

    @staticmethod
    async def on_dispatcher_shutdown(
        dispatcher: Dispatcher | None = None, bot: Bot | None = None
    ) -> None:
        if dispatcher and bot:
            await dispatcher.emit_shutdown(bot=bot, **dispatcher.workflow_data)

    def _setup_api_router_v1(self) -> None:
        api_router_v1: APIRouter = APIRouter(
            on_startup=(
                functools.partial(
                    self.on_dispatcher_startup,
                    dispatcher=self._dispatcher_v1,
                    bot=self._bot_v1,
                ),
            ),
            on_shutdown=(
                functools.partial(
                    self.on_dispatcher_shutdown,
                    dispatcher=self._dispatcher_v1,
                    bot=self._bot_v1,
                ),
            ),
        )
        api_router_v1.include_router(router=healthcheck_router_v1, tags=["v1"])
        api_router_v1.include_router(router=telegram_webhook_router_v1, tags=["v1"])
        self._app.include_router(
            router=api_router_v1, prefix=f"/{app_settings.api_path_v1}"
        )

    def _setup_api_middlewares(self) -> None:
        self._app.add_middleware(LoggingMiddleware)

    def _setup_api_exception_handlers(self) -> None:
        self._app.add_exception_handler(
            HTTPException, ExceptionHandler.http_exception_handler
        )
        self._app.add_exception_handler(
            RequestValidationError, ExceptionHandler.handle_request_validation_error
        )
        self._app.add_exception_handler(AppError, ExceptionHandler.handle_app_error)

    def _setup_api_event_handlers(self) -> None:
        self._app.add_event_handler("startup", self.on_app_startup)
        self._app.add_event_handler("shutdown", self.on_app_shutdown)

    async def on_app_startup(self) -> None:
        logger.info("Starting Application startup...")
        if telegram_settings.mode == UpdateMethod.POLLING.value:
            logger.info("Starting Telegram Polling...")
            try:
                await self._bot_v1.delete_webhook(drop_pending_updates=True)
                logger.info("Existing Telegram webhook deleted.")
            except Exception as error:
                logger.error(f"Error while deleting webhook: {error}")
            polling_task = create_task(self._dispatcher_v1.start_polling(self._bot_v1))
            self._app.state.polling_task_v1 = polling_task
        elif telegram_settings.mode == UpdateMethod.WEBHOOK.value:
            logger.info("Starting Telegram Webhook...")
            try:
                await self._task_queue_consumer.start()
            except Exception as error:
                logger.error(f"Error while starting TaskQueueConsumer: {error}")
                raise

        await self._mongodb.init_database(document_models=get_documments())

        logger.info("Application started successfully.")

    async def on_app_shutdown(self) -> None:
        logger.info("Starting Application shutdown...")
        if telegram_settings.mode == UpdateMethod.POLLING.value:
            polling_task = getattr(self._app.state, "polling_task_v1", None)
            if polling_task:
                polling_task.cancel()
                logger.info("Telegram Polling task cancelled.")

        if self._dispatcher_v1 and self._bot_v1:
            await self._dispatcher_v1.emit_shutdown(
                bot=self._bot_v1, **self._dispatcher_v1.workflow_data
            )
        if self._task_queue_consumer:
            await self._task_queue_consumer.stop()
        if self._bot_v1:
            await self._bot_v1.session.close()
        if self._mongodb:
            await self._mongodb.close()
        logger.info("Application shut down successfully.")

    @property
    def app(self) -> FastAPI:
        return self._app
