from typing import Optional

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
    CommonModel,
    DataResponseModel,
    PaginationModel,
    optional_field,
)


class Workflow(CommonModel):
    name: str
    note: Optional[str]
    context: Optional[dict]
    managed: bool
    default: bool
    disabled: bool
    context_schema: Optional[dict]


class WorkflowDataResponse(DataResponseModel[Workflow]):
    pass


class WorkflowListResponse(PaginationModel[Workflow]):
    pass


class WorkflowCreateRequest(BaseModel):
    name: str
    note: Optional[str] = None
    context: Optional[dict] = None
    default: bool = False
    disabled: bool = False
    managed: bool = False
    context_schema: Optional[dict] = None


class WorkflowUpdateRequest(BaseModel):
    name: str = optional_field
    note: Optional[str] = optional_field
    context: Optional[dict] = optional_field
    default: bool = optional_field
    disabled: bool = optional_field
    context_schema: Optional[dict] = optional_field
