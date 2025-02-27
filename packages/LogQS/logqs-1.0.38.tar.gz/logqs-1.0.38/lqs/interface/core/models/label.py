from typing import Optional

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
    CommonModel,
    DataResponseModel,
    PaginationModel,
    optional_field,
)


class Label(CommonModel):
    value: str
    note: Optional[str]


class LabelDataResponse(DataResponseModel[Label]):
    pass


class LabelListResponse(PaginationModel[Label]):
    pass


class LabelCreateRequest(BaseModel):
    value: str
    note: Optional[str] = None


class LabelUpdateRequest(BaseModel):
    value: str = optional_field
    note: Optional[str] = optional_field
