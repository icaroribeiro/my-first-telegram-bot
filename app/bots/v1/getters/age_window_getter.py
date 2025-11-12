from aiogram_dialog import (
    DialogManager,
)


async def age_window_getter(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict:
    name = dialog_manager.dialog_data.get("name", "Guest")
    return {
        "name": name,
    }
