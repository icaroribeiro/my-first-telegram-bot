from asyncio import Queue
from typing import TypeVar

from app.infrastructure.task_queue.models.task_item_model import TaskItemModel

T = TypeVar("T", bound="TaskItemModel")


class TaskQueue(Queue):
    def __init__(self, max_size: int = 0) -> None:
        super().__init__(maxsize=max_size)

    async def put_item(self, item: T) -> None:
        await self.put(item=item)

    async def get_item(self) -> T:
        return await self.get()

    def check_size(self) -> int:
        return self.qsize()
