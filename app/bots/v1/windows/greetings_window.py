from aiogram.types import ContentType
from aiogram_dialog import (
    Window,
)
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from app.bots.v1.getters.greetings_window_getter import greetings_window_getter
from app.bots.v1.handlers.greetings_handler import greetings_handler
from app.bots.v1.handlers.other_type_handler import (
    other_type_handler,
)
from app.bots.v1.state_groups.bmi_dialog_state_group import BMIDialogSG

greetings_window = Window(
    Format("{message}"),
    MessageInput(greetings_handler, content_types=[ContentType.TEXT]),
    MessageInput(other_type_handler),
    state=BMIDialogSG.greeting,
    getter=greetings_window_getter,
)
