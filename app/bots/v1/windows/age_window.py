from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Counter, Next
from aiogram_dialog.widgets.text import Format

from app.bots.v1.getters.age_window_getter import age_window_getter
from app.bots.v1.handlers.age_change_handler import age_change_handler
from app.bots.v1.handlers.age_next_button_handler import age_next_button_handler
from app.bots.v1.state_groups.bmi_dialog_state_group import BMIDialogSG

age_window = Window(
    Format("Please enter your age below (1-120):"),
    Counter(
        id="age_counter",
        default=18,
        min_value=1,
        max_value=120,
        increment=1,
        on_text_click=age_change_handler,
    ),
    Next(
        text=Format("Next (Height) ➡️"),
        id="next_to_height",
        on_click=age_next_button_handler,
        when="is_age_set",
    ),
    state=BMIDialogSG.age,
    getter=age_window_getter,
)
