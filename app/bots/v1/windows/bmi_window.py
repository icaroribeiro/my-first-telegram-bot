from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from app.bots.v1.getters.bmi_window_getter import bmi_window_getter
from app.bots.v1.state_groups.bmi_dialog_state_group import BMIDialogSG

bmi_window = Window(
    Format("--- ✨ Your BMI Results ✨ ---"),
    Format(""),
    Format("Your Body Mass Index is: <b>{bmi_index}</b>"),
    Format("Classification: <b>{bmi_category}</b>"),
    Format(""),
    Button(
        text=Format("Finish and Exit 👋"),
        id="finish_bmi_calc",
        on_click=None,
    ),
    state=BMIDialogSG.bmi,
    getter=bmi_window_getter,
)
