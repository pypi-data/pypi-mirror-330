from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
    CommonModel,
    DataResponseModel,
    PaginationModel,
    ProcessState,
    ProcessType,
    optional_field,
)


class Hook(CommonModel):
    workflow_id: UUID
    trigger_process: ProcessType
    trigger_state: ProcessState
    name: Optional[str]
    note: Optional[str]
    context: Optional[dict]
    managed: bool
    disabled: bool
    uri: Optional[str]


class HookDataResponse(DataResponseModel[Hook]):
    pass


class HookListResponse(PaginationModel[Hook]):
    pass


class HookCreateRequest(BaseModel):
    trigger_process: ProcessType
    trigger_state: ProcessState
    name: Optional[str] = None
    note: Optional[str] = None
    context: Optional[dict] = None
    disabled: bool = False
    managed: bool = False
    uri: Optional[str] = None
    secret: Optional[str] = None


class HookUpdateRequest(BaseModel):
    trigger_process: ProcessType = optional_field
    trigger_state: ProcessState = optional_field
    name: Optional[str] = optional_field
    note: Optional[str] = optional_field
    context: Optional[dict] = optional_field
    disabled: bool = optional_field
    uri: Optional[str] = optional_field
    secret: Optional[str] = optional_field
