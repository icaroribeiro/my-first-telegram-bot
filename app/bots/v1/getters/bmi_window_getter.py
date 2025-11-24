from aiogram_dialog import DialogManager

from app.core.logging.logger import get_logger
from app.infrastructure.mongodb.documents.bmi_record_document import CategoryName

logger = get_logger()


async def bmi_window_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    bmi_index = dialog_manager.dialog_data.get("bmi_index", "N/A")
    category = dialog_manager.dialog_data.get("bmi_category", CategoryName.UNKNOWN)

    match category:
        case CategoryName.NORMAL_WEIGHT.value:
            category_display = f"🟢 {category} 🟢"
        case CategoryName.OVERWEIGHT.value:
            category_display = f"⚠️ {category} ⚠️"
        case CategoryName.UNDERWEIGHT.value:
            category_display = f"⚠️ {category} ⚠️"
        case CategoryName.OBESE.value:
            category_display = f"🔴 {category} 🔴"
        case _:
            category_display = category

    return {
        "bmi_index": bmi_index,
        "bmi_category": category_display,
    }
