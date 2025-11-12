import functools
import secrets
import uuid
from typing import Annotated, Any

from aiogram import Bot, Dispatcher
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, Request, Response, status

from app.api.v1.dtos.webhook_dto import WebhookDTO
from app.app_error import AppError
from app.core.container.container import Container
from app.core.logging.logger import get_logger
from app.core.settings.app_settings import get_app_settings
from app.core.settings.telegram_settings import get_telegram_settings
from app.infrastructure.task_queue.models.task_item_model import TaskItemModel
from app.infrastructure.task_queue.task_queue_producer import TaskQueueProducer
from app.services.telegram_webhook_service import TelegramWebhookService

logger = get_logger()
app_settings = get_app_settings()
telegram_settings = get_telegram_settings()

api_router = APIRouter(
    include_in_schema=False,
)


@api_router.post(
    f"/{telegram_settings.webhook_path_v1}/{telegram_settings.bot_token_v1}",
    status_code=status.HTTP_200_OK,
)
@inject
async def post_webhook(
    request: Request,
    response: Response,
    x_telegram_bot_api_webhook_secret: Annotated[
        str | None, Header(alias="x-telegram-bot-api-secret-token")
    ] = None,
    telegram_webhook_service: TelegramWebhookService = Depends(
        Provide[Container.telegram_webhook_service]
    ),
    task_queue_producer: TaskQueueProducer = Depends(
        Provide[Container.task_queue_producer]
    ),
) -> Response:
    try:
        bot: Bot = request.app.state.bot_v1
        dispatcher: Dispatcher = request.app.state.dispatcher_v1
    except AttributeError:
        message = "Bot or Dispatcher not found in app state. App initialization failed."
        logger.error(message)
        raise AppError(
            message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    verify_secret: bool = secrets.compare_digest(
        x_telegram_bot_api_webhook_secret, telegram_settings.webhook_secret_v1
    )
    if not verify_secret:
        message = f"Invalid secret token received: {x_telegram_bot_api_webhook_secret}"
        logger.warning(message)
        raise AppError(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

    json_data: dict[str, Any]
    try:
        json_data = await request.json()
        logger.info(f"JSON parsed from request successfully: {json_data}")
    except Exception as error:
        message = f"Error while parsing JSON from request: {error}"
        logger.error(message)
        raise AppError(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    task_item: TaskItemModel
    try:
        task_item = await task_queue_producer.produce_task(
            id=uuid.uuid4(),
            async_func=functools.partial(
                telegram_webhook_service.handle_webhook,
                json_data=json_data,
                dispatcher=dispatcher,
                bot=bot,
            ),
        )
    except Exception as error:
        message = f"Error while producing a Task: {error}"
        logger.error(message)
        raise AppError(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )

    webhook_dto = WebhookDTO(task_id=str(task_item.id), json_data=json_data)
    message = f"Webhook handled successfully: {webhook_dto}"
    logger.info(message)
    response.status_code = status.HTTP_200_OK
    return response
