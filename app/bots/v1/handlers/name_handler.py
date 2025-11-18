from aiogram.types import Message
from aiogram_dialog import (
    DialogManager,
)
from aiogram_dialog.widgets.input import MessageInput

from app.core.logging.logger import get_logger

logger = get_logger()


async def name_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data["name"] = message.text
    await message.answer(f"Nice to meet you, {message.text}")
    await dialog_manager.next()
