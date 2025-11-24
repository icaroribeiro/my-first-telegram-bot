from pydantic import Field

from app.infrastructure.mongodb.documents.bmi_category_document import (
    BMICategoryBaseDocument,
    StyleTag,
)
from beanie import iterative_migration


class OldBMICategoryDocument(BMICategoryBaseDocument):
    pass


class NewBMICategoryDocument(BMICategoryBaseDocument):
    min_bmi: float = Field(
        default=0, description="Minimum BMI index for this category (inclusive)."
    )
    max_bmi: float | None = Field(
        default=None,
        description="Maximum BMI index for this category (exclusive). Use None for the highest category.",
    )
    category_name: str = Field(
        default="Unknown", description="The friendly name of the BMI category."
    )
    style_tag: StyleTag = Field(
        default=StyleTag.UNKNOWN.value,
        description="A short tag for styling/emoji (e.g., 'normal', 'warning', 'severe').",
    )


class Forward:
    @iterative_migration()
    async def upgrade(
        self,
        input_document: OldBMICategoryDocument,
        output_document: NewBMICategoryDocument,
    ):
        pass


class Backward:
    @iterative_migration()
    async def downgrade(
        self,
        input_document: OldBMICategoryDocument,
        output_document: NewBMICategoryDocument,
    ):
        pass
