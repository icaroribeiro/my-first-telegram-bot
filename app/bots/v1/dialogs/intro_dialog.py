from aiogram_dialog import (
    Dialog,
)

from app.bots.v1.getters.bmi_dialog_getter import intro_dialog_getter
from app.bots.v1.windows.age_window import age_window
from app.bots.v1.windows.finish_window import finish_window
from app.bots.v1.windows.greetings_window import (
    greetings_window,
)

intro_dialog = Dialog(
    greetings_window, age_window, finish_window, getter=intro_dialog_getter
)
