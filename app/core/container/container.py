from dependency_injector import containers, providers

from app.core.settings.mongodb_settings import get_mongodb_settings
from app.core.settings.task_queue_settings import get_task_queue_settings
from app.infrastructure.mongodb.mongodb import MongoDB
from app.infrastructure.task_queue.task_queue import TaskQueue
from app.infrastructure.task_queue.task_queue_consumer import TaskQueueConsumer
from app.infrastructure.task_queue.task_queue_producer import TaskQueueProducer
from app.services.healthcheck_service import HealthCheckService
from app.services.telegram_webhook_service import TelegramWebhookService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    task_queue = providers.Singleton(
        TaskQueue, max_size=get_task_queue_settings().queue_max_size
    )

    task_queue_producer = providers.Singleton(TaskQueueProducer, task_queue=task_queue)

    task_queue_consumer = providers.Singleton(
        TaskQueueConsumer,
        task_queue=task_queue,
        max_retries=get_task_queue_settings().max_retries,
        initial_backoff_seconds=get_task_queue_settings().initial_backoff_seconds,
        async_task_timeout_seconds=get_task_queue_settings().async_task_timeout_seconds,
    )

    mongodb = providers.Singleton(MongoDB, mongodb_settings=get_mongodb_settings())

    healthcheck_service = providers.Singleton(HealthCheckService, mongodb=mongodb)

    telegram_webhook_service = providers.Singleton(TelegramWebhookService)
