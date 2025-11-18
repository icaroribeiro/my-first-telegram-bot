from aiogram_dialog import (
    DialogManager,
)


async def greetings_window_getter(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict:
    name = dialog_manager.dialog_data.get("name", "Guest")
    message = "Greeting! Please, introduce yourself:"
    return {
        "name": name,
        "message": message,
    }
