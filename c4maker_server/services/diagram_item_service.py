from datetime import datetime
from uuid import UUID

from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
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
        DiagramItemService.__prepare_to_persist(diagram_item, user)
        self.diagram_item_repository.create(diagram_item)

    def update_diagram_item(self, diagram_item: DiagramItem, user: User):
        DiagramItemService.__prepare_to_persist(diagram_item, user)
        self.diagram_item_repository.update(diagram_item)

    def delete_diagram_item(self, diagram_item_id: UUID, user: User):
        diagram_item = self.find_diagram_item_by_id(diagram_item_id)

        DiagramItemService.__prepare_to_persist(diagram_item, user)
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

        return self.diagram_item_repository.find_all_by_diagram(diagram_id)

    @staticmethod
    def __prepare_to_persist(diagram_item: DiagramItem, user: User):
        DiagramItemService.__check_permission_to_persist(diagram_item, user)
        diagram_item.set_track_data(user, datetime.now())

    @staticmethod
    def __check_permission_to_persist(diagram_item: DiagramItem, user: User):
        if user.allowed_to_edit(diagram_item.diagram):
            return

        raise PermissionException("DiagramItem", diagram_item.id, user)
