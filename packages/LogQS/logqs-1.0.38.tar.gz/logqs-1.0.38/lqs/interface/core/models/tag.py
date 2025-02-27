from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
    CommonModel,
    DataResponseModel,
    PaginationModel,
    optional_field,
    Int64,
)


class Tag(CommonModel):
    label_id: UUID
    log_id: UUID
    topic_id: Optional[UUID]

    note: Optional[str]
    context: Optional[dict]
    start_time: Optional[Int64]
    end_time: Optional[Int64]


class TagDataResponse(DataResponseModel[Tag]):
    pass


class TagListResponse(PaginationModel[Tag]):
    pass


class TagCreateRequest(BaseModel):
    label_id: UUID
    topic_id: Optional[UUID] = None

    note: Optional[str] = None
    context: Optional[dict] = None
    start_time: Optional[Int64] = None
    end_time: Optional[Int64] = None


class TagUpdateRequest(BaseModel):
    label_id: UUID = optional_field
    topic_id: Optional[UUID] = optional_field

    note: Optional[str] = optional_field
    context: Optional[dict] = optional_field
    start_time: Optional[Int64] = optional_field
    end_time: Optional[Int64] = optional_field
