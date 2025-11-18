from typing import Any

from aiogram_dialog import (
    ChatEvent,
    DialogManager,
)


async def on_age_changed_handler(
    callback: ChatEvent,
    select: Any,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["age"] = item_id
    await dialog_manager.next()
