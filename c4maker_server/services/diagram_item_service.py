from datetime import datetime
from typing import Optional
from uuid import UUID

from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.diagram_service import DiagramService
from c4maker_server.services.ports.diagram_item_repository import DiagramItemRepository


class DiagramItemService:
    diagram_item_repository: DiagramItemRepository
    diagram_service: DiagramService

    def __init__(self, diagram_item_repository: DiagramItemRepository, diagram_service: DiagramService):
        self.diagram_item_repository = diagram_item_repository
        self.diagram_service = diagram_service

    def create_diagram_item(self, diagram_item: DiagramItem, user: User):
        self.__prepare_to_persist(diagram_item, user)
        self.diagram_item_repository.create(diagram_item)

    def update_diagram_item(self, diagram_item: DiagramItem, user: User):
        persisted_diagram_item = self.find_diagram_item_by_id(diagram_item.id)
        self.__prepare_to_persist(diagram_item, user, persisted_diagram_item=persisted_diagram_item)

        self.diagram_item_repository.update(diagram_item)

    def delete_diagram_item(self, diagram_item_id: UUID, user: User):
        diagram_item = self.find_diagram_item_by_id(diagram_item_id)

        self.__prepare_to_persist(diagram_item, user)
        self.diagram_item_repository.delete(diagram_item_id)

    def find_diagram_item_by_id(self, diagram_item_id: UUID) -> DiagramItem:
        diagram_item = self.diagram_item_repository.find_by_id(diagram_item_id)

        if not diagram_item:
            raise EntityNotFoundException("DiagramItem", diagram_item_id)

        return diagram_item

    def find_diagram_items_by_diagram(self, diagram_id: UUID, user: User):
        diagram = self.diagram_service.find_diagram_by_id(diagram_id, user)

        if not user.allowed_to_view(diagram):
            raise PermissionException("Diagram", diagram_id, user)

        return self.diagram_item_repository.find_all_by_diagram(diagram)

    def __prepare_to_persist(self, diagram_item: DiagramItem, user: User, is_delete: bool = False,
                             persisted_diagram_item: Optional[DiagramItem] = None):
        diagram = self.diagram_service.find_diagram_by_id(diagram_item.diagram.id, user)
        diagram_item.diagram = diagram

        self.__check_permission_to_persist(persisted_diagram_item if persisted_diagram_item else diagram_item, user)

        if is_delete:
            return

        DiagramItemService.__check_missing_fields(diagram_item, persisted_diagram_item)

        if persisted_diagram_item:
            diagram_item.created_by = persisted_diagram_item.created_by
            diagram_item.created_at = persisted_diagram_item.created_at
            diagram_item.modified_by = persisted_diagram_item.modified_by
            diagram_item.modified_at = persisted_diagram_item.modified_at

        diagram_item.set_track_data(user, datetime.now())

    @staticmethod
    def __check_missing_fields(diagram_item: DiagramItem, persisted_diagram_item: Optional[DiagramItem]):
        missing_fields = []

        if persisted_diagram_item and diagram_item.diagram != persisted_diagram_item.diagram:
            missing_fields.append("diagram")
        if not diagram_item.diagram:
            missing_fields.append("diagram")
        if not diagram_item.name:
            missing_fields.append("name")
        if not diagram_item.details:
            missing_fields.append("details")
        if not diagram_item.item_description:
            missing_fields.append("item_description")

        if missing_fields:
            raise InvalidEntityException("DiagramItem", missing_fields)

    def __check_permission_to_persist(self, diagram_item: DiagramItem, user: User):
        self.diagram_service.check_permission_to_persist(diagram_item.diagram, user)
