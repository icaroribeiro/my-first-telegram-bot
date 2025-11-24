from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.bots.v1.state_groups.bmi_dialog_state_group import BMIDialogSG


async def age_next_button_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    """
    Este handler força o fim do diálogo atual e inicia o próximo em uma
    mensagem totalmente nova, garantindo que a mensagem de confirmação
    de texto apareça ANTES da próxima janela interativa.
    """

    # 1. Recupera o valor da idade
    final_age = dialog_manager.dialog_data.get("age", "N/A")
    confirmation_text = (
        f"✅ Idade confirmada: {final_age} anos. Por favor, insira a sua altura."
    )

    # 2. TERMINA O DIÁLOGO ATUAL. Isso remove a interface interativa da Idade da mensagem original.
    # É crucial fazer isso ANTES de qualquer novo start, para evitar conflitos de edição.
    await dialog_manager.done()

    # 3. Envia uma mensagem de confirmação para o chat. Esta é uma NOVA MENSAGEM de texto puro.
    await callback.message.answer(confirmation_text)

    # 4. INICIA O PRÓXIMO DIÁLOGO/WINDOW (Altura).
    # O uso de 'new_stack=True' força o Aiogram Dialog a enviar uma NOVA MENSAGEM
    # para esta janela, em vez de tentar editar a mensagem anterior.
    await dialog_manager.start(BMIDialogSG.height, new_stack=True)

    # 5. Notificação de callback (opcional)
    await callback.answer("Transição concluída.")
