from uuid import UUID
from typing import Optional

from lqs.interface.core import DeleteInterface
from lqs.client.common import RESTInterface

# TODO: make this consistent with other interfaces


class Delete(DeleteInterface, RESTInterface):
    service: str = "lqs"

    def __init__(self, app):
        super().__init__(app=app)

    def _api_key(self, api_key_id: UUID):
        self._delete_resource(f"apiKeys/{api_key_id}")
        return

    def _digestion(self, digestion_id: UUID, lock_token: Optional[str] = None):
        self._delete_resource(
            f"digestions/{digestion_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _digestion_part(
        self,
        digestion_id: UUID,
        digestion_part_id: UUID,
        lock_token: Optional[str] = None,
    ):
        self._delete_resource(
            f"digestions/{digestion_id}/parts/{digestion_part_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _digestion_topic(
        self,
        digestion_id: UUID,
        digestion_topic_id: UUID,
        lock_token: Optional[str] = None,
    ):
        self._delete_resource(
            f"digestions/{digestion_id}/topics/{digestion_topic_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _group(self, group_id: UUID, lock_token: Optional[str] = None):
        self._delete_resource(
            f"groups/{group_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _hook(self, workflow_id: UUID, hook_id: UUID):
        self._delete_resource(f"workflows/{workflow_id}/hooks/{hook_id}")
        return

    def _ingestion(self, ingestion_id: UUID, lock_token: Optional[str] = None):
        self._delete_resource(
            f"ingestions/{ingestion_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _ingestion_part(
        self,
        ingestion_id: UUID,
        ingestion_part_id: UUID,
        lock_token: Optional[str] = None,
    ):
        self._delete_resource(
            f"ingestions/{ingestion_id}/parts/{ingestion_part_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _label(self, label_id: UUID):
        self._delete_resource(f"labels/{label_id}")
        return

    def _log(self, log_id: UUID, lock_token: Optional[str] = None):
        self._delete_resource(
            f"logs/{log_id}", additiona_params={"lock_token": lock_token}
        )
        return

    def _log_object(
        self, log_id: UUID, object_key: str, lock_token: Optional[str] = None
    ):
        self._delete_resource(
            f"logs/{log_id}/objects/{object_key}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _object(self, object_store_id: UUID, object_key: str):
        raise NotImplementedError

    def _object_store(self, object_store_id: UUID):
        self._delete_resource(f"objectStores/{object_store_id}")
        return

    def _query(self, log_id: UUID, query_id: UUID, lock_token: Optional[str] = None):
        self._delete_resource(
            f"logs/{log_id}/queries/{query_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _record(
        self, timestamp: float, topic_id: UUID, lock_token: Optional[str] = None
    ):
        self._delete_resource(
            f"topics/{topic_id}/records/{timestamp}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _role(self, role_id: UUID):
        self._delete_resource(f"roles/{role_id}")
        return

    def _tag(self, log_id: UUID, tag_id: UUID, lock_token: Optional[str] = None):
        self._delete_resource(
            f"logs/{log_id}/tags/{tag_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _topic(self, topic_id: UUID, lock_token: Optional[str] = None):
        self._delete_resource(
            f"topics/{topic_id}",
            additiona_params={"lock_token": lock_token},
        )
        return

    def _user(self, user_id: UUID):
        self._delete_resource(f"users/{user_id}")
        return

    def _workflow(self, workflow_id: UUID):
        self._delete_resource(f"workflows/{workflow_id}")
        return
