from aiogram.types import Message
from aiogram_dialog import (
    DialogManager,
    StartMode,
)

from app.bots.v1.state_groups.bmi_dialog_state_group import BMIDialogSG


async def start_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=BMIDialogSG.greeting,
        mode=StartMode.RESET_STACK,
        data={
            "user_id": message.from_user.id,
            "language_code": message.from_user.language_code,
        },
    )
