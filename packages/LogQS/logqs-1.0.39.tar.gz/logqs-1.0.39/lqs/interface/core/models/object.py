from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from lqs.interface.base.models.__common__ import (
    ResourceModel,
    UploadState,
)


class Object(ResourceModel["Object"]):
    _repr_fields = ("key",)

    key: str
    etag: Optional[str]
    size: Optional[int]
    last_modified: Optional[datetime]
    presigned_url: Optional[str]
    upload_state: UploadState


class ObjectDataResponse(BaseModel):
    data: Object


class ObjectListResponse(BaseModel):
    data: List[Object]
    is_truncated: Optional[bool]
    key_count: Optional[int]
    max_keys: int

    continuation_token: Optional[str]
    next_continuation_token: Optional[str]
    prefix: Optional[str]
    start_after: Optional[str]
    delimiter: Optional[str]
    common_prefixes: Optional[List[str]]


class ObjectCreateRequest(BaseModel):
    key: str
    content_type: Optional[str] = None


class ObjectUpdateRequest(BaseModel):
    upload_state: UploadState


# Object Parts


class ObjectPart(BaseModel):
    part_number: int
    etag: str
    size: int
    last_modified: Optional[datetime]
    presigned_url: Optional[str]


class ObjectPartDataResponse(BaseModel):
    data: ObjectPart


class ObjectPartListResponse(BaseModel):
    data: List[ObjectPart]
    part_number_marker: Optional[int]
    next_part_number_marker: Optional[int]
    max_parts: Optional[int]
    is_truncated: Optional[bool]


class ObjectPartCreateRequest(BaseModel):
    part_number: Optional[int] = None
    size: int
