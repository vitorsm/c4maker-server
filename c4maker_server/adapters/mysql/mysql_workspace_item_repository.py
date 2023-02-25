from typing import Optional, List
from uuid import UUID

from c4maker_server.adapters.models.workspace_item_db import WorkspaceItemDB
from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.domain.entities.workspace_item import WorkspaceItem
from c4maker_server.services.ports.workspace_item_repository import WorkspaceItemRepository


class MySQLWorkspaceItemRepository(WorkspaceItemRepository):

    def __init__(self, mysql_client: MySQLClient):
        self.mysql_client = mysql_client

    def create(self, workspace_item: WorkspaceItem):
        workspace_item_db = WorkspaceItemDB(workspace_item)
        self.mysql_client.add(workspace_item_db)

    def update(self, workspace_item: WorkspaceItem):
        workspace_item_db = self.__find_db_obj_by_id(str(workspace_item.id))
        workspace_item_db.update_properties(workspace_item)
        self.mysql_client.update(workspace_item_db)

    def delete(self, workspace_item_id: UUID):
        workspace_item_db = self.__find_db_obj_by_id(str(workspace_item_id))

        if not workspace_item_db:
            return

        self.mysql_client.delete(workspace_item_db)

    def find_by_id(self, workspace_item_id: UUID) -> Optional[WorkspaceItem]:
        workspace_item_db = self.__find_db_obj_by_id(str(workspace_item_id))

        if not workspace_item_db:
            return None

        return workspace_item_db.to_entity()

    def find_items_by_workspace(self, workspace_id: UUID) -> List[WorkspaceItem]:
        workspace_items_db = self.mysql_client.db.session.query(WorkspaceItemDB)\
            .filter(WorkspaceItemDB.workspace_id == str(workspace_id))

        return [w.to_entity() for w in workspace_items_db]

    def __find_db_obj_by_id(self, workspace_item_id: str) -> WorkspaceItemDB:
        return self.mysql_client.db.session.query(WorkspaceItemDB).get(workspace_item_id)
