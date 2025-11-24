from enum import Enum

from pydantic import Field

from app.infrastructure.mongodb.documents.base_document import BaseDocument
from app.infrastructure.mongodb.documents.bmi_record_document import CategoryName


class StyleTag(str, Enum):
    NORMAL = "Normal"
    WARNING = "Warning"
    SEVERE = "Severe"
    UNKNOWN = "Unknown"


class BMICategoryBaseDocument(BaseDocument):
    class Settings:
        name: str = "bmi_categories"
        indexes = [
            ("min_bmi", "max_bmi"),
        ]


class BMICategoryDocument(BMICategoryBaseDocument):
    min_bmi: float = Field(
        description="Minimum BMI index for this category (inclusive)."
    )
    max_bmi: float | None = Field(
        default=None,
        description="Maximum BMI index for this category (exclusive). Use None for the highest category.",
    )
    category_name: CategoryName = Field(
        description="The friendly name of the BMI category."
    )
    style_tag: StyleTag = Field(
        default=StyleTag.UNKNOWN,
        description="A short tag for styling/emoji (e.g., 'normal', 'warning', 'severe').",
    )
