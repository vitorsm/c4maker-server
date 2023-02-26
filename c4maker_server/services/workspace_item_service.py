import uuid
from datetime import datetime
from typing import Optional, List

from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.workspace_item import WorkspaceItem
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.ports.authentication_repository import AuthenticationRepository
from c4maker_server.services.ports.workspace_item_repository import WorkspaceItemRepository
from c4maker_server.services.workspace_service import WorkspaceService


class WorkspaceItemService:

    def __init__(self, workspace_item_repository: WorkspaceItemRepository,
                 authentication_repository: AuthenticationRepository, workspace_service: WorkspaceService):
        self.workspace_item_repository = workspace_item_repository
        self.workspace_service = workspace_service
        self.authentication_repository = authentication_repository

    def create_or_update_workspace_item(self, workspace_item: WorkspaceItem, user: Optional[User] = None):
        persisted_workspace_item = None

        if not user:
            user = self.authentication_repository.get_current_user()

        if workspace_item.id:
            persisted_workspace_item = self.find_workspace_item_by_id(workspace_item.id, user)

        if persisted_workspace_item:
            self.update_workspace_item(workspace_item, user, persisted_workspace_item)
        else:
            self.create_workspace_item(workspace_item, user)

    def create_workspace_item(self, workspace_item: WorkspaceItem, user: Optional[User] = None):
        if not user:
            user = self.authentication_repository.get_current_user()

        self.__prepare_to_persist(workspace_item, user)
        self.workspace_item_repository.create(workspace_item)

    def update_workspace_item(self, workspace_item: WorkspaceItem, user: Optional[User] = None,
                              persisted_workspace_item: Optional[WorkspaceItem] = None):
        if not user:
            user = self.authentication_repository.get_current_user()

        if not persisted_workspace_item:
            persisted_workspace_item = self.find_workspace_item_by_id(workspace_item.id, user)

        self.__prepare_to_persist(workspace_item, user,
                                  persisted_workspace_item=persisted_workspace_item)

        self.workspace_item_repository.update(workspace_item)

    def delete_workspace_item(self, workspace_item_id: uuid.UUID):
        user = self.authentication_repository.get_current_user()
        workspace_item = self.find_workspace_item_by_id(workspace_item_id, user)

        self.__prepare_to_persist(workspace_item, user, is_delete=True)
        self.workspace_item_repository.delete(workspace_item_id)

    def find_workspace_item_by_id(self, workspace_item_id: uuid.UUID, user: Optional[User] = None) -> WorkspaceItem:
        if not user:
            user = self.authentication_repository.get_current_user()

        workspace_item = self.workspace_item_repository.find_by_id(workspace_item_id)

        if not workspace_item:
            raise EntityNotFoundException("WorkspaceItem", workspace_item_id)

        if not user.allowed_to_view(workspace_item.workspace):
            raise PermissionException("WorkspaceItem", workspace_item_id, user)

        return workspace_item

    def find_items_by_workspace(self, workspace_id: uuid.UUID, user: Optional[User] = None) -> List[WorkspaceItem]:
        self.workspace_service.find_workspace_by_id(workspace_id, user)
        return self.workspace_item_repository.find_items_by_workspace(workspace_id)

    def __prepare_to_persist(self, workspace_item: WorkspaceItem, user: User, is_delete: bool = False,
                             persisted_workspace_item: Optional[WorkspaceItem] = None):
        workspace = self.workspace_service.find_workspace_by_id(workspace_item.workspace.id, user) \
            if workspace_item.workspace else None

        workspace_item.workspace = workspace

        WorkspaceItemService.check_missing_fields(workspace_item, persisted_workspace_item)
        self.__check_permission_to_persist(persisted_workspace_item if persisted_workspace_item else workspace_item,
                                           user)

        if is_delete:
            return

        WorkspaceItemService.check_missing_fields(workspace_item, persisted_workspace_item)

        workspace_item.set_track_data(user, datetime.now())

        if persisted_workspace_item:
            workspace_item.created_by = persisted_workspace_item.created_by
            workspace_item.created_at = persisted_workspace_item.created_at
        else:
            workspace_item.id = uuid.uuid4()

    @staticmethod
    def check_missing_fields(workspace_item: WorkspaceItem, persisted_workspace_item: Optional[WorkspaceItem]):
        missing_fields = list()

        if not workspace_item.workspace_item_type:
            missing_fields.append("workspace_item_type")
        if not workspace_item.name:
            missing_fields.append("name")
        if not workspace_item.details:
            missing_fields.append("details")
        if not workspace_item.description:
            missing_fields.append("description")
        if not workspace_item.key:
            missing_fields.append("key")
        if not workspace_item.workspace or \
                persisted_workspace_item and workspace_item.workspace != persisted_workspace_item.workspace:
            missing_fields.append("workspace")

        if missing_fields:
            raise InvalidEntityException("WorkspaceItem", missing_fields)

    @staticmethod
    def __check_permission_to_persist(workspace_item: WorkspaceItem, user: User):
        WorkspaceService.check_permission_to_persist(workspace_item.workspace, user)
