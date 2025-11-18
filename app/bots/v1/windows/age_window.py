from aiogram_dialog import (
    Window,
)
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format

from app.bots.v1.getters.age_window_getter import age_window_getter
from app.bots.v1.handlers.on_age_changed_handler import (
    on_age_changed_handler,
)
from app.bots.v1.state_groups.intro_dialog_state_group import (
    IntroDialogSG,
)

age_window = Window(
    Format("{name}! How old are you?"),
    Select(
        Format("{item}"),
        items=["0-12", "12-18", "18-25", "25-40", "40+"],
        item_id_getter=lambda x: x,
        id="intro_age_select",
        on_click=on_age_changed_handler,
    ),
    state=IntroDialogSG.age,
    getter=age_window_getter,
    preview_data={"name": "Ícaro"},
)
