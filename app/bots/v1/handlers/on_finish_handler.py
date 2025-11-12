from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager,
)
from aiogram_dialog.widgets.kbd import Button

from app.core.logging.logger import get_logger

logger = get_logger()


async def on_finish_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    if dialog_manager.is_preview():
        await dialog_manager.done()
        return
    await callback.message.answer("Thank you. To start again click /start")
    await dialog_manager.done()
