import abc
from typing import Optional, List
from uuid import UUID

from c4maker_server.domain.entities.workspace_item import WorkspaceItem


class WorkspaceItemRepository(metaclass=abc.ABCMeta):

    def create(self, workspace_item: WorkspaceItem):
        raise NotImplementedError

    def update(self, workspace_item: WorkspaceItem):
        raise NotImplementedError

    def delete(self, workspace_item_id: UUID):
        raise NotImplementedError

    def find_by_id(self, workspace_item_id: UUID) -> Optional[WorkspaceItem]:
        raise NotImplementedError

    def find_items_by_workspace(self, workspace_id: UUID) -> List[WorkspaceItem]:
        raise NotImplementedError
