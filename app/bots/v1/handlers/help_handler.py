from typing import Optional

from aiogram.types import Message
from aiogram_dialog import DialogManager


async def help_handler(
    message: Message, dialog_manager: Optional[DialogManager] = None
) -> None:
    """
    Handles the /help command. Provides information about the bot's commands
    and checks if the user is currently inside an active aiogram-dialog.
    """
    help_text = (
        "🤖 **Comandos Disponíveis:**\n"
        "/start - Iniciar a interação principal e ver o menu.\n"
        "/help - Exibir este guia de comandos e instruções.\n"
        "/exit - Cancelar a operação atual e sair do diálogo.\n\n"
        "---"
    )

    # Check if a dialog manager exists and has a current state
    if dialog_manager and dialog_manager.has_context():
        dialog_info = dialog_manager.current_context().state.split(":")

        # aiogram_dialog states are usually formatted as 'DialogName:StateName'
        current_dialog_name = (
            dialog_info[0] if len(dialog_info) > 0 else "Diálogo Ativo"
        )
        current_state_name = dialog_info[-1]

        context_message = (
            f"⚠️ Você está atualmente no diálogo: **{current_dialog_name}** "
            f"(Estado: `{current_state_name}`).\n"
            "Pode continuar respondendo, ou use **/exit** para sair."
        )
    else:
        context_message = (
            "Pronto para começar! Use **/start** para iniciar uma nova conversa."
        )

    final_message = f"{help_text}\n{context_message}"

    await message.answer(final_message, parse_mode="Markdown")
