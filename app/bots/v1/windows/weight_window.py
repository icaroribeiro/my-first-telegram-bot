from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Counter, Next
from aiogram_dialog.widgets.text import Format

from app.bots.v1.getters.weight_window_getter import weight_window_getter
from app.bots.v1.handlers.weight_change_handler import weight_change_handler
from app.bots.v1.state_groups.bmi_dialog_state_group import BMIDialogSG

weight_window = Window(
    Format("Please enter your weight in pounds (1 lb ≈ 0.45 kg)."),
    Counter(
        id="bmi_weight_counter",
        default=150,
        min_value=1,
        max_value=1000,
        increment=1,
        on_text_click=weight_change_handler,
    ),
    Next(text=Format("Calculate BMI ✨"), when="is_weight_set"),
    state=BMIDialogSG.weight,
    getter=weight_window_getter,
)
