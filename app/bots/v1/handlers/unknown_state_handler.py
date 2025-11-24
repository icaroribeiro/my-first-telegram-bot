from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)

from app.bots.v1.state_groups.bmi_dialog_state_group import BMIDialogSG
from app.core.logging.logger import get_logger

logger = get_logger()


async def unknown_state_handler(event, dialog_manager: DialogManager):
    logger.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        BMIDialogSG.greeting,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
