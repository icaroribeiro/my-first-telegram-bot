from aiogram_dialog import (
    DialogManager,
)


async def finish_window_getter(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict:
    name = dialog_manager.dialog_data.get("name", "Guest")
    age = dialog_manager.dialog_data.get("age", "0")
    can_smoke = age in ("18-25", "25-40", "40+")
    return {
        "name": name,
        "can_smoke": can_smoke,
    }
