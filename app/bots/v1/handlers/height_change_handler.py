from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCounter

from app.core.logging.logger import get_logger

logger = get_logger()


async def height_change_handler(
    callback: CallbackQuery,
    widget: ManagedCounter,
    dialog_manager: DialogManager,
) -> None:
    height_value = widget.get_value()
    dialog_manager.dialog_data["height_in_inches"] = height_value
    await callback.answer(f"Height set to: {height_value} inches")
