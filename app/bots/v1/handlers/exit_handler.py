from aiogram.types import Message
from aiogram_dialog import (
    DialogManager,
)


async def exit_handler(message: Message, dialog_manager: DialogManager) -> None:
    try:
        await dialog_manager.stop()
    except AttributeError:
        await dialog_manager.done()
    await message.answer(
        "Você saiu do fluxo de diálogo principal do bot. Use o comando /start para recomeçar."
    )
