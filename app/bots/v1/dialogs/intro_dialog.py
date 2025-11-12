from aiogram_dialog import (
    Dialog,
    DialogManager,
)

from app.bots.v1.getters.intro_dialog_getter import intro_dialog_getter
from app.bots.v1.windows.age_window import age_window
from app.bots.v1.windows.finish_window import finish_window
from app.bots.v1.windows.greetings_window import (
    greetings_window,
)


async def intro_dialog_get_data(dialog_manager: DialogManager, **kwargs) -> dict:
    data_from_start = dialog_manager.start_data
    return {
        "user_telegram_id": data_from_start.get("user_id"),
        "common_status": "Active",
    }


intro_dialog = Dialog(
    greetings_window, age_window, finish_window, getter=intro_dialog_getter
)
