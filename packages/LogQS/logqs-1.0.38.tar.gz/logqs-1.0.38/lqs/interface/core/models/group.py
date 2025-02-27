from typing import List, Optional
from uuid import UUID

from lqs.interface.core.models.__common__ import (
    CommonModel,
    DataResponseModel,
    LockModel,
    LockCreateRequest,
    LockUpdateRequest,
    PaginationModel,
    optional_field,
)
from lqs.interface.core.models import Log


class Group(CommonModel, LockModel):
    name: str
    note: Optional[str]
    context: Optional[dict]
    default_workflow_id: Optional[UUID]

    def list_logs(self, **kwargs) -> List["Log"]:
        return self._app.list.logs(group_id=self.id, **kwargs).data


class GroupDataResponse(DataResponseModel[Group]):
    pass


class GroupListResponse(PaginationModel[Group]):
    pass


class GroupCreateRequest(LockCreateRequest):
    name: str
    note: Optional[str] = None
    context: Optional[dict] = None
    default_workflow_id: Optional[UUID] = None


class GroupUpdateRequest(LockUpdateRequest):
    name: str = optional_field
    note: Optional[str] = optional_field
    context: Optional[dict] = optional_field
    default_workflow_id: Optional[UUID] = optional_field
