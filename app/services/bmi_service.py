# You must import this:
from app.core.logging.logger import get_logger
from app.infrastructure.mongodb.documents.bmi_category_document import (
    BMICategoryDocument,
    StyleTag,
)
from app.infrastructure.mongodb.documents.bmi_record_document import CategoryName

logger = get_logger()


class BMIService:
    def __init__(self, bmi_category_document: BMICategoryDocument):
        self._bmi_category_document = bmi_category_document

    async def calculate_bmi_and_categorize(
        self, height_in_inches: float, weight_in_pounds: float
    ) -> tuple[float, CategoryName, StyleTag]:
        bmi_index = self.calculate_index(
            height_in_inches=height_in_inches, weight_in_pounds=weight_in_pounds
        )

        if bmi_index == 0.0:
            return 0.0, CategoryName.UNKNOWN, StyleTag.UNKNOWN

        category, style_tag = await self.get_category(bmi_index)

        return bmi_index, category, style_tag

    def calculate_index(
        self, height_in_inches: float, weight_in_pounds: float
    ) -> float:
        if height_in_inches <= 0 or weight_in_pounds <= 0:
            return 0.0

        bmi_index = round(weight_in_pounds / (height_in_inches**2) * 703, 2)

        return bmi_index

    async def get_category(self, bmi_index: float) -> tuple[str, str]:
        bmi_category_doc = await self._bmi_category_document.find_one(
            {
                "min_bmi": {"$lte": bmi_index},
                "$or": [
                    {"max_bmi": None},
                    {"max_bmi": {"$gt": bmi_index}},
                ],
            }
        )

        if bmi_category_doc:
            return bmi_category_doc.category_name, bmi_category_doc.style_tag

        return CategoryName.UNKNOWN, StyleTag.UNKNOWN
