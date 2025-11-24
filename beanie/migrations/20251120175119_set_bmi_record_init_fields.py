from pydantic import Field

from app.infrastructure.mongodb.documents.bmi_record_document import (
    BMIRecordBaseDocument,
    CategoryName,
)
from beanie import iterative_migration


class OldBMIRecordDocument(BMIRecordBaseDocument):
    pass


class NewBMIRecordDocument(BMIRecordBaseDocument):
    user_id: int = Field(default=0, description="Telegram User ID.")
    height_in_inches: float = Field(default=0, description="User's height in inches.")
    weight_in_pounds: float = Field(default=0, description="User's weight in pounds.")
    bmi_index: float = Field(default=0, description="Calculated Body Mass Index.")
    category_name: CategoryName = Field(
        default=CategoryName.UNKNOWN.value,
        description="BMI category (e.g., Normal, Overweight).",
    )


class Forward:
    @iterative_migration()
    async def upgrade(
        self,
        input_document: OldBMIRecordDocument,
        output_document: NewBMIRecordDocument,
    ):
        pass


class Backward:
    @iterative_migration()
    async def downgrade(
        self,
        input_document: OldBMIRecordDocument,
        output_document: NewBMIRecordDocument,
    ):
        pass
