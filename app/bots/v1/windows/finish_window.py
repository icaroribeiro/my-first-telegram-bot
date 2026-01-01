from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Row, Start, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.bots.v1.getters.finish_window_getter import finish_window_getter
from app.bots.v1.handlers.finish_handler import (
    finish_handler,
)
from app.bots.v1.state_groups.bmi_dialog_state_group import (
    BMIDialogSG,
)

finish_window = Window(
    Multi(
        Format("{name}! Thank you for your answers."),
        Const("Hope you are not smoking", when="can_smoke"),
        sep="\n\n",
    ),
    Row(
        Back(),
        SwitchTo(Const("Restart"), id="restart", state=BMIDialogSG.greeting),
        Start(text=Const("Calculate BMI ✨"), id="start_bmi", state=BMIDialogSG.height),
        Button(Const("Finish"), on_click=finish_handler, id="finish"),
    ),
    state=BMIDialogSG.finish,
    getter=finish_window_getter,
)
