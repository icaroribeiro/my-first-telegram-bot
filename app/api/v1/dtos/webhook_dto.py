from typing import Any

from pydantic import BaseModel, Field


class WebhookDTO(BaseModel):
    message: str = Field(default="Handled")
    task_id: str
    json_data: dict[str, Any]
