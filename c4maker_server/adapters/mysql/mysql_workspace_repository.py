from typing import List, Optional
from uuid import UUID

from c4maker_server.adapters.models import UserAccessDB
from c4maker_server.adapters.models.workspace_db import WorkspaceDB
from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.services.ports.workspace_repository import WorkspaceRepository


class MySQLWorkspaceRepository(WorkspaceRepository):

    def __init__(self, mysql_client: MySQLClient):
        self.mysql_client = mysql_client

    def create(self, workspace: Workspace):
        workspace_db = WorkspaceDB(workspace)
        self.mysql_client.add(workspace_db)

    def update(self, workspace: Workspace):
        workspace_db = self.__find_db_obj_by_id(str(workspace.id))
        workspace_db.update_properties(workspace)
        self.mysql_client.update(workspace)

    def delete(self, workspace_id: UUID):
        workspace_db = self.__find_db_obj_by_id(str(workspace_id))

        if not workspace_db:
            return

        self.mysql_client.delete(workspace_db)

    def find_by_id(self, workspace_id: UUID) -> Optional[Workspace]:
        workspace_db = self.__find_db_obj_by_id(str(workspace_id))

        if not workspace_db:
            return None

        return workspace_db.to_entity()

    def find_all_by_user(self, user: User) -> List[Workspace]:
        user_accesses_db = self.mysql_client.db.session.query(UserAccessDB).filter(UserAccessDB.user_id == str(user.id))
        workspaces_created_by_user = \
            self.mysql_client.db.session.query(WorkspaceDB).filter(WorkspaceDB.created_by == str(user.id))

        workspaces = [user_access_db.workspace.to_entity() for user_access_db in user_accesses_db]
        workspaces.extend([diagram.to_entity() for diagram in workspaces_created_by_user])

        return workspaces

    def __find_db_obj_by_id(self, workspace_id: str) -> WorkspaceDB:
        return self.mysql_client.db.session.query(WorkspaceDB).get(workspace_id)
