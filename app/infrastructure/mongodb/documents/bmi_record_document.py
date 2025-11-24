from enum import Enum

from pydantic import Field

from app.infrastructure.mongodb.documents.base_document import BaseDocument


class CategoryName(str, Enum):
    NORMAL_WEIGHT = "Normal Weight"
    OVERWEIGHT = "Overweight"
    UNDERWEIGHT = "Underweight"
    OBESE = "Obese"
    UNKNOWN = "Unknown"


class BMIRecordBaseDocument(BaseDocument):
    class Settings:
        name: str = "bmi_records"
        indexes = [
            ("user_id", "created_at"),
        ]


class BMIRecordDocument(BMIRecordBaseDocument):
    user_id: int = Field(description="Telegram User ID.")
    height_in_inches: float = Field(description="User's height in inches.")
    weight_in_pounds: float = Field(description="User's weight in pounds.")
    bmi_index: float = Field(description="Calculated Body Mass Index.")
    category_name: CategoryName = Field(
        default=CategoryName.UNKNOWN,
        description="BMI category (e.g., Normal Weight, Overweight).",
    )
