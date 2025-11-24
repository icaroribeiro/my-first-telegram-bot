from aiogram_dialog import DialogManager

from app.core.logging.logger import get_logger

logger = get_logger()


async def age_window_getter(dialog_manager: DialogManager, **kwargs):
    is_age_set = dialog_manager.dialog_data.get("age") is not None
    return {"is_age_set": is_age_set}
