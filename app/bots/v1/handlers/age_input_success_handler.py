from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput  # Used for type hinting

MIN_AGE = 1
MAX_AGE = 120
DEFAULT_AGE = 18


async def age_input_success_handler(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    age_value: int,
):
    """
    Handles successful integer input from TextInput.
    NOTE: This handler MUST take 4 arguments, as required by TextInput.on_success.
    """
    if MIN_AGE <= age_value <= MAX_AGE:
        dialog_manager.dialog_data["age_error"] = None
        dialog_manager.dialog_data["age_value"] = age_value
    else:
        error_message = f"🛑 Error: Age must be between {MIN_AGE} and {MAX_AGE}."
        dialog_manager.dialog_data["age_error"] = error_message
        dialog_manager.dialog_data["age_value"] = age_value

    await dialog_manager.switch_to(dialog_manager.current_state())
