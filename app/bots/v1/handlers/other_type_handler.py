from aiogram.types import Message
from aiogram_dialog import (
    DialogManager,
)
from aiogram_dialog.widgets.input import MessageInput


async def other_type_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    await message.answer("Text is expected")
