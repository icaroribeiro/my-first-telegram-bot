from app.infrastructure.mongodb.documents.webhook_event_document import (
    WebhookEventDocument,
)
from beanie import iterative_migration


class Forward:
    @iterative_migration
    async def upgrade(self):
        await WebhookEventDocument.init()


class Backward:
    @iterative_migration
    async def downgrade(self):
        await WebhookEventDocument.drop_collection()
