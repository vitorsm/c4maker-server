import abc
from typing import Optional, List
from uuid import UUID

from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.workspace import Workspace


class WorkspaceRepository(metaclass=abc.ABCMeta):
    def create(self, workspace: Workspace):
        raise NotImplementedError

    def update(self, workspace: Workspace):
        raise NotImplementedError

    def delete(self, workspace_id: UUID):
        raise NotImplementedError

    def find_by_id(self, workspace_id: UUID) -> Optional[Workspace]:
        raise NotImplementedError

    def find_all_by_user(self, user: User) -> List[Workspace]:
        raise NotImplementedError
