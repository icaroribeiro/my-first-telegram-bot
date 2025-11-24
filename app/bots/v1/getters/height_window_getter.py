from aiogram_dialog import DialogManager

from app.core.logging.logger import get_logger

logger = get_logger()


async def height_window_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    is_height_set = dialog_manager.dialog_data.get("height_in_inches") is not None
    return {"is_height_set": is_height_set}
