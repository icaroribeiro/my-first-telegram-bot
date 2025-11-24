from aiogram_dialog import DialogManager

from app.core.logging.logger import get_logger

logger = get_logger()


async def weight_window_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    is_weight_set = dialog_manager.dialog_data.get("weight_in_pounds") is not None
    return {"is_weight_set": is_weight_set}
