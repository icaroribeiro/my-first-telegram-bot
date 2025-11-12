import uuid
from typing import Any, Awaitable, Callable

from app.core.logging.logger import get_logger
from app.infrastructure.task_queue.models.task_item_model import TaskItemModel
from app.infrastructure.task_queue.task_queue import TaskQueue

logger = get_logger()


class TaskQueueProducer:
    def __init__(self, task_queue: TaskQueue) -> None:
        self.task_queue = task_queue

    async def produce_task(
        self, id: uuid.UUID, async_func: Callable[[Any], Awaitable[bool]]
    ) -> TaskItemModel:
        logger.info("Starting producing a Task...")
        task_item: TaskItemModel = TaskItemModel(id=id, async_func=async_func)
        await self.task_queue.put_item(item=task_item)
        logger.info(f"{task_item} produced successfully.")
        return task_item
