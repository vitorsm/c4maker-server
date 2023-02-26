import uuid
from datetime import datetime
from typing import Optional, List

from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.ports.authentication_repository import AuthenticationRepository
from c4maker_server.services.ports.workspace_repository import WorkspaceRepository


class WorkspaceService:
    def __init__(self, workspace_repository: WorkspaceRepository, authentication_repository: AuthenticationRepository):
        self.workspace_repository = workspace_repository
        self.authentication_repository = authentication_repository

    def create_workspace(self, workspace: Workspace):
        WorkspaceService.__prepare_to_persist(workspace, self.authentication_repository.get_current_user())
        self.workspace_repository.create(workspace)

    def update_workspace(self, workspace: Workspace):
        user = self.authentication_repository.get_current_user()
        persisted_workspace = self.find_workspace_by_id(workspace.id, user)

        WorkspaceService.__prepare_to_persist(workspace, user, persisted_workspace=persisted_workspace)
        self.workspace_repository.update(workspace)

    def delete_workspace(self, workspace_id: uuid.UUID):
        user = self.authentication_repository.get_current_user()

        workspace = self.find_workspace_by_id(workspace_id, user)
        WorkspaceService.__prepare_to_persist(workspace, user, is_delete=True)

        self.workspace_repository.delete(workspace_id)

    def find_workspace_by_id(self, workspace_id: uuid.UUID, user: Optional[User] = None) -> Workspace:
        if not user:
            user = self.authentication_repository.get_current_user()

        workspace = self.workspace_repository.find_by_id(workspace_id)

        if not workspace:
            raise EntityNotFoundException("Workspace", workspace_id)

        if not user.allowed_to_view(workspace):
            raise PermissionException("Workspace", workspace_id, user)

        return workspace

    def find_workspaces_by_user(self) -> List[Workspace]:
        return self.workspace_repository.find_all_by_user(self.authentication_repository.get_current_user())

    @staticmethod
    def __prepare_to_persist(workspace: Workspace, user: User, is_delete: bool = False,
                             persisted_workspace: Optional[Workspace] = None):
        WorkspaceService.check_permission_to_persist(persisted_workspace if persisted_workspace else workspace, user,
                                                     is_delete)

        if is_delete:
            return

        workspace.set_track_data(user, datetime.now())

        if persisted_workspace:
            workspace.created_by = persisted_workspace.created_by
            workspace.created_at = persisted_workspace.created_at
        else:
            workspace.id = uuid.uuid4()

        WorkspaceService.__check_required_fields(workspace)

    @staticmethod
    def __check_required_fields(workspace: Workspace):
        if not workspace.name:
            raise InvalidEntityException("Workspace", ["name"])

    @staticmethod
    def check_permission_to_persist(workspace: Workspace, user: User, is_delete: bool = False):
        if not workspace.id:
            return

        # to delete an item the user must be the owner
        if is_delete and user.is_owner(workspace) or not is_delete and user.allowed_to_edit(workspace):
            return

        raise PermissionException("Workspace", workspace.id, user)
