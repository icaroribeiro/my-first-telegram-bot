from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Counter, Next
from aiogram_dialog.widgets.text import Format

from app.bots.v1.getters.height_window_getter import height_window_getter
from app.bots.v1.handlers.height_change_handler import height_change_handler
from app.bots.v1.state_groups.bmi_dialog_state_group import BMIDialogSG

height_window = Window(
    Format("Please enter your height in inches (1 inch = 2.54 cm)."),
    Counter(
        id="bmi_height_counter",
        default=65,
        min_value=1,
        max_value=100,
        increment=1,
        on_text_click=height_change_handler,
    ),
    Next(text=Format("Next (Weight) ➡️"), when="is_height_set"),
    state=BMIDialogSG.height,
    getter=height_window_getter,
)
