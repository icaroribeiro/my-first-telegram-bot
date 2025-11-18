from aiogram_dialog import (
    DialogManager,
)


async def intro_dialog_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    data_from_start = dialog_manager.start_data
    user_id = data_from_start.get("user_id")
    return {
        "user_telegram_id": user_id,
        "common_status": "Active",
    }
