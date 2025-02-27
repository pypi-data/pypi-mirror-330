from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
    DataResponseModel,
    CommonModel,
    PaginationModel,
    optional_field,
    Int64,
)


class DigestionTopic(CommonModel):
    digestion_id: UUID
    topic_id: UUID
    start_time: Optional[Int64]
    end_time: Optional[Int64]
    frequency: Optional[float]
    query_data_filter: Optional[dict]
    context_filter: Optional[dict]


class DigestionTopicDataResponse(DataResponseModel[DigestionTopic]):
    pass


class DigestionTopicListResponse(PaginationModel[DigestionTopic]):
    pass


class DigestionTopicCreateRequest(BaseModel):
    topic_id: UUID
    start_time: Optional[Int64]
    end_time: Optional[Int64]
    frequency: Optional[float] = None
    query_data_filter: Optional[dict] = None
    context_filter: Optional[dict] = None


class DigestionTopicUpdateRequest(BaseModel):
    start_time: Optional[Int64] = optional_field
    end_time: Optional[Int64] = optional_field
    frequency: Optional[float] = optional_field
    query_data_filter: Optional[dict] = optional_field
    context_filter: Optional[dict] = optional_field
