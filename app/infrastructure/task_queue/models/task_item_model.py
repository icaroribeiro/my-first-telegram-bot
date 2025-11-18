import uuid
from typing import Any, Awaitable, Callable

from pydantic import BaseModel, Field


class TaskItemModel(BaseModel):
    id: uuid.UUID = Field(description="Uniqeu idetifier for the task")
    async_func: Callable[[Any], Awaitable[bool]] = Field(
        description="The async function to execute."
    )

    class Config:
        arbitrary_types_allowed = True

    def __str__(self) -> str:
        return f"TaskItemModel(id=({self.id})"
