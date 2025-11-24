from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCounter

from app.core.logging.logger import get_logger

logger = get_logger()


async def age_change_handler(
    callback: CallbackQuery,
    widget: ManagedCounter,
    dialog_manager: DialogManager,
) -> None:
    age_value = widget.get_value()
    dialog_manager.dialog_data["age"] = age_value
    await callback.answer(f"Age set to: {age_value} years.")
