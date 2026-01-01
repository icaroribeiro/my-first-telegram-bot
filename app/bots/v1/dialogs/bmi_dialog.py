from aiogram_dialog import Dialog

from app.bots.v1.getters.bmi_dialog_getter import bmi_dialog_getter
from app.bots.v1.windows.age_window import age_window
from app.bots.v1.windows.bmi_window import bmi_window
from app.bots.v1.windows.finish_window import finish_window
from app.bots.v1.windows.greetings_window import (
    greetings_window,
)
from app.bots.v1.windows.height_window import height_window
from app.bots.v1.windows.weight_window import weight_window

bmi_dialog = Dialog(
    greetings_window,
    age_window,
    height_window,
    weight_window,
    bmi_window,
    finish_window,
    getter=bmi_dialog_getter,
)
