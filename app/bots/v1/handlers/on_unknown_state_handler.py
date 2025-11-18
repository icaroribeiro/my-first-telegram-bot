from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)

from app.bots.v1.state_groups.intro_dialog_state_group import (
    IntroDialogSG,
)
from app.core.logging.logger import get_logger

logger = get_logger()


async def on_unknown_state_handler(event, dialog_manager: DialogManager):
    logger.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        IntroDialogSG.greeting,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
