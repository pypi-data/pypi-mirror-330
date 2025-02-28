from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
    CommonModel,
    DataResponseModel,
    PaginationModel,
    optional_field,
)


class Query(CommonModel):
    log_id: UUID
    name: Optional[str]
    note: Optional[str]
    context: Optional[dict]

    statement: Optional[str]
    parameters: Optional[Dict[str, Any]]
    columns: Optional[List[str]]
    rows: Optional[List[List[Any]]]
    error: Optional[dict]


class QueryDataResponse(DataResponseModel[Query]):
    pass


class QueryListResponse(PaginationModel[Query]):
    pass


class QueryCreateRequest(BaseModel):
    name: Optional[str] = None
    note: Optional[str] = None
    context: Optional[dict] = None
    statement: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class QueryUpdateRequest(BaseModel):
    name: Optional[str] = optional_field
    note: Optional[str] = optional_field
    context: Optional[dict] = optional_field
    statement: Optional[str] = optional_field
    parameters: Optional[Dict[str, Any]] = optional_field
