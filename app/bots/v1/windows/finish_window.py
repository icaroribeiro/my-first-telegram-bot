from aiogram_dialog import (
    Window,
)
from aiogram_dialog.widgets.kbd import Back, Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.bots.v1.getters.finish_window_getter import finish_window_getter
from app.bots.v1.handlers.on_finish_handler import (
    on_finish_handler,
)
from app.bots.v1.state_groups.intro_dialog_state_group import (
    IntroDialogSG,
)

finish_window = Window(
    Multi(
        Format("{name}! Thank you for your answers."),
        Const("Hope you are not smoking", when="can_smoke"),
        sep="\n\n",
    ),
    Row(
        Back(),
        SwitchTo(Const("Restart"), id="restart", state=IntroDialogSG.greeting),
        Button(Const("Finish"), on_click=on_finish_handler, id="finish"),
    ),
    state=IntroDialogSG.finish,
    getter=finish_window_getter,
)
