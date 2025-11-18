from typing import Any, Dict

from pydantic import Field

from app.infrastructure.mongodb.documents.base_document import BaseDocument


class WebhookEventDocument(BaseDocument):
    payload: Dict[str, Any] = Field(
        ...,
        description="Webhook event payload",
    )

    class Settings:
        name = "webhook_events"
