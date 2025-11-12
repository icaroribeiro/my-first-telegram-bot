from typing import Any

from aiogram_dialog import (
    DialogManager,
)


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    age = dialog_manager.dialog_data.get("age", None)
    return {
        "name": dialog_manager.dialog_data.get("name", ""),
        "age": age,
        "can_smoke": age in ("18-25", "25-40", "40+"),
    }
