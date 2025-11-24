from functools import lru_cache
from typing import Type

from beanie import Document

from .bmi_category_document import BMICategoryDocument
from .bmi_record_document import BMIRecordDocument


@lru_cache
def get_documments() -> list[Type[Document]]:
    return [BMICategoryDocument, BMIRecordDocument]
