from aiogram.types import Message
from aiogram_dialog import DialogManager


async def age_input_error_handler(
    message: Message,
    widget,
    dialog_manager: DialogManager,
):
    """
    Handles errors when the text input cannot be converted to the required type.
    """
    error_message = "O valor inserido não é um número válido. Por favor, digite sua idade ou use os botões +/-."
    dialog_manager.dialog_data["age_error"] = error_message

    # FIX: Force the dialog window to refresh to show the error
    await dialog_manager.update(data={"error_message": error_message})
