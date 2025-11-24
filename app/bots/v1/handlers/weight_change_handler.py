from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCounter
from dependency_injector.wiring import Provide, inject

from app.core.container.container import Container
from app.core.logging.logger import get_logger
from app.infrastructure.mongodb.documents.bmi_record_document import (
    BMIRecordDocument,
)
from app.services.bmi_service import BMIService

logger = get_logger()


@inject
async def weight_change_handler(
    event: CallbackQuery,
    widget: ManagedCounter,
    dialog_manager: DialogManager,
    bmi_service: BMIService = Provide[Container.bmi_service],
) -> None:
    try:
        weight_value = widget.get_value()
        dialog_manager.dialog_data["weight_in_pounds"] = weight_value
        await event.answer(f"Weight set to: {weight_value} pounds")

        height = dialog_manager.dialog_data.get("height_in_inches")
        weight = dialog_manager.dialog_data.get("weight_in_pounds")
        user_id = event.from_user.id

        if not height or not weight:
            await event.answer("Error: Missing height or weight data.", show_alert=True)
            return

        bmi_index, category, style_tag = await bmi_service.calculate_bmi_and_categorize(
            height_in_inches=float(height), weight_in_pounds=float(weight)
        )

        bmi_record = BMIRecordDocument(
            user_id=user_id,
            height_in_inches=float(height),
            weight_in_pounds=float(weight),
            bmi_index=bmi_index,
            category_name=category,
        )
        await bmi_record.insert()

        dialog_manager.dialog_data["bmi_index"] = bmi_index
        dialog_manager.dialog_data["bmi_category"] = category.value
    except Exception as error:
        message = f"Error while setting weight: {error}"
        logger.error(message)
        raise Exception(message)
