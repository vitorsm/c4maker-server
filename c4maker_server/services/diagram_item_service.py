import uuid
from typing import Optional, List
from uuid import UUID

from c4maker_server.domain.entities.c4_diagram_item import C4DiagramItem
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.workspace_item import WorkspaceItem
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.diagram_service import DiagramService
from c4maker_server.services.ports.authentication_repository import AuthenticationRepository
from c4maker_server.services.ports.diagram_item_repository import DiagramItemRepository
from c4maker_server.services.workspace_item_service import WorkspaceItemService
from c4maker_server.services.workspace_service import WorkspaceService


VALID_DIAGRAM_ITEM_INSTANCES = [C4DiagramItem]


class DiagramItemService:
    def __init__(self, diagram_item_repository: DiagramItemRepository,
                 authentication_repository: AuthenticationRepository,
                 diagram_service: DiagramService,
                 workspace_item_service: WorkspaceItemService):
        self.diagram_item_repository = diagram_item_repository
        self.diagram_service = diagram_service
        self.authentication_repository = authentication_repository
        self.workspace_item_service = workspace_item_service

    def create_diagram_item(self, diagram_item: DiagramItem):
        user = self.authentication_repository.get_current_user()

        self.__create_or_update_workspace_item(diagram_item.workspace_item, user)

        self.__prepare_to_persist(diagram_item, user)
        self.diagram_item_repository.create(diagram_item)

    def update_diagram_item(self, diagram_item: DiagramItem):
        user = self.authentication_repository.get_current_user()

        self.__create_or_update_workspace_item(diagram_item.workspace_item, user)

        self.__prepare_to_persist(diagram_item, user)

        self.diagram_item_repository.update(diagram_item)

    def delete_diagram_item(self, diagram_item_id: UUID):
        user = self.authentication_repository.get_current_user()
        diagram_item = self.find_diagram_item_by_id(diagram_item_id, user)

        self.__prepare_to_persist(diagram_item, user)
        self.diagram_item_repository.delete(diagram_item_id)

    def find_diagram_item_by_id(self, diagram_item_id: UUID, user: Optional[User] = None) -> DiagramItem:
        if not user:
            user = self.authentication_repository.get_current_user()

        diagram_item = self.diagram_item_repository.find_by_id(diagram_item_id)

        if not diagram_item:
            raise EntityNotFoundException("DiagramItem", diagram_item_id)

        if not user.allowed_to_view(diagram_item.workspace_item.workspace):
            raise PermissionException("DiagramItem", diagram_item_id, user)

        return diagram_item

    def find_diagram_items_by_diagram(self, diagram_id: UUID) -> List[DiagramItem]:
        user = self.authentication_repository.get_current_user()

        try:
            diagram = self.diagram_service.find_diagram_by_id(diagram_id, user)
        except PermissionException:
            raise PermissionException("Diagram", diagram_id, user)

        return self.diagram_item_repository.find_all_by_diagram(diagram)

    def __create_or_update_workspace_item(self, workspace_item: WorkspaceItem, user: User):
        try:
            self.workspace_item_service.create_or_update_workspace_item(workspace_item, user)
        except EntityNotFoundException:
            raise InvalidEntityException("DiagramItem", ["workspace_item"])

    def __prepare_to_persist(self, diagram_item: DiagramItem, user: User, is_delete: bool = False,
                             persisted_diagram_item: Optional[DiagramItem] = None):

        if not any(isinstance(diagram_item, instance) for instance in VALID_DIAGRAM_ITEM_INSTANCES):
            raise InvalidEntityException("DiagramItem", ['diagram_item_type'])

        diagram = self.diagram_service.find_diagram_by_id(diagram_item.diagram.id, user) \
            if diagram_item.diagram else None
        parent_diagram_item = self.find_diagram_item_by_id(diagram_item.parent.id, user) \
            if diagram_item.parent else None
        if not persisted_diagram_item and diagram_item.id:
            persisted_diagram_item = self.diagram_item_repository.find_by_id(diagram_item.id)

        diagram_item.diagram = diagram
        diagram_item.parent = parent_diagram_item

        DiagramItemService.__check_missing_fields(diagram_item, persisted_diagram_item)

        # todo - if the diagram is null, we will have an exception
        self.__check_permission_to_persist(persisted_diagram_item if persisted_diagram_item else diagram_item, user)

        if is_delete:
            return

        DiagramItemService.__check_missing_fields(diagram_item, persisted_diagram_item)
        DiagramItemService.__check_relationship_consistency(diagram_item)

        if not persisted_diagram_item:
            diagram_item.id = uuid.uuid4()

    @staticmethod
    def __check_missing_fields(diagram_item: DiagramItem, persisted_diagram_item: Optional[DiagramItem]):
        missing_fields = []
        persisted_workspace_item = persisted_diagram_item.workspace_item if persisted_diagram_item else None

        if not diagram_item.diagram or \
                persisted_diagram_item and diagram_item.diagram != persisted_diagram_item.diagram:
            missing_fields.append("diagram")

        # todo - test this condition
        if not diagram_item.workspace_item or \
                diagram_item.diagram and diagram_item.workspace_item.workspace != diagram_item.diagram.workspace:
            missing_fields.append("workspace_item")
        else:
            try:
                WorkspaceItemService.check_missing_fields(diagram_item.workspace_item, persisted_workspace_item)
            except InvalidEntityException as ex:
                missing_fields.append(ex.missing_fields)

        if diagram_item.parent and diagram_item.parent.diagram != diagram_item.diagram:
            missing_fields.append("parent")

        if missing_fields:
            raise InvalidEntityException("DiagramItem", missing_fields)

    @staticmethod
    def __check_relationship_consistency(diagram_item: DiagramItem):
        # todo - check if the diagram item in relationship is a valid entity
        if not diagram_item.relationships:
            return

        has_relationship_with_different_type = any(relationship.DIAGRAM_ITEM_TYPE != diagram_item.DIAGRAM_ITEM_TYPE
                                                   for relationship in diagram_item.relationships)

        if has_relationship_with_different_type:
            raise InvalidEntityException("DiagramItem", ['relationships'])

    @staticmethod
    def __check_permission_to_persist(diagram_item: DiagramItem, user: User):
        WorkspaceService.check_permission_to_persist(diagram_item.diagram.workspace, user)
