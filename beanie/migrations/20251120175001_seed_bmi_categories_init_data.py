from pydantic import Field
from pymongo.asynchronous.client_session import AsyncClientSession

from app.core.logging.logger import get_logger
from app.infrastructure.mongodb.documents.bmi_category_document import (
    BMICategoryBaseDocument,
    StyleTag,
)
from app.infrastructure.mongodb.documents.bmi_record_document import CategoryName
from beanie import free_fall_migration

logger = get_logger()


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
    category_name: CategoryName = Field(
        default=CategoryName.UNKNOWN,
        description="The friendly name of the BMI category.",
    )
    style_tag: StyleTag = Field(
        default=StyleTag.UNKNOWN,
        description="A short tag for styling/emoji (e.g., 'normal', 'warning', 'severe').",
    )


class Forward:
    @free_fall_migration(document_models=[NewBMICategoryDocument])
    async def upgrade(self, session: AsyncClientSession | None = None):
        collection_name: str = ""
        try:
            collection_name = BMICategoryBaseDocument.Settings.name
            logger.info(
                f"Starting checking the number of documents in collection '{collection_name}'..."
            )
            count = await NewBMICategoryDocument.count()
            if count > 0:
                logger.info(
                    f"Documents already exist in collection '{collection_name}'. Skipping initial data seed."
                )
                return
        except Exception as error:
            message = f"Error while checking the number of documents in collection '{collection_name}': {error}"
            logger.error(message)
            raise Exception(message)

        try:
            logger.info(
                f"Starting seeding initial data in collection {collection_name}..."
            )
            bmi_categories_data = [
                NewBMICategoryDocument(
                    min_bmi=0.0,
                    max_bmi=18.5,
                    category_name=CategoryName.UNDERWEIGHT,
                    style_tag=StyleTag.WARNING,
                ),
                NewBMICategoryDocument(
                    min_bmi=18.5,
                    max_bmi=25.0,
                    category_name=CategoryName.NORMAL_WEIGHT,
                    style_tag=StyleTag.NORMAL,
                ),
                NewBMICategoryDocument(
                    min_bmi=25.0,
                    max_bmi=30.0,
                    category_name=CategoryName.OVERWEIGHT,
                    style_tag=StyleTag.WARNING,
                ),
                NewBMICategoryDocument(
                    min_bmi=30.0,
                    max_bmi=None,
                    category_name=CategoryName.OBESE,
                    style_tag=StyleTag.SEVERE,
                ),
            ]
            await NewBMICategoryDocument.insert_many(
                documents=bmi_categories_data, session=session
            )
            logger.info(f"All documents from collection '{collection_name}' deleted.")
        except Exception as error:
            message = f"Error while seeding initial data in collection '{collection_name}': {error}"
            logger.error(message)
            raise Exception(message)


class Backward:
    @free_fall_migration(document_models=[NewBMICategoryDocument])
    async def downgrade(self, session: AsyncClientSession | None = None):
        collection_name: str = ""
        try:
            collection_name = BMICategoryBaseDocument.Settings.name
            logger.info(
                f"Starting deleting documents from collection '{collection_name}'..."
            )
            category_names_to_delete = [
                CategoryName.UNDERWEIGHT.value,
                CategoryName.NORMAL_WEIGHT.value,
                CategoryName.OVERWEIGHT.value,
                CategoryName.OBESE.value,
            ]
            await NewBMICategoryDocument.delete_many(
                {"category_name": {"$in": category_names_to_delete}},
                session=session,
            )
            logger.info(f"All documents from collection '{collection_name}' deleted.")
        except Exception as error:
            message = f"Error while deleting documents from collection '{collection_name}': {error}"
            logger.error(message)
            raise Exception(message)
