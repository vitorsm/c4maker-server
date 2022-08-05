import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.ports.authentication_repository import AuthenticationRepository
from c4maker_server.services.ports.diagram_repository import DiagramRepository


class DiagramService:
    diagram_repository: DiagramRepository

    def __init__(self, diagram_repository: DiagramRepository, authentication_repository: AuthenticationRepository):
        self.diagram_repository = diagram_repository
        self.authentication_repository = authentication_repository

    def create_diagram(self, diagram: Diagram):
        DiagramService.__prepare_to_persist(diagram, self.authentication_repository.get_current_user())
        self.diagram_repository.create(diagram)

    def update_diagram(self, diagram: Diagram):
        user = self.authentication_repository.get_current_user()
        persisted_diagram = self.find_diagram_by_id(diagram.id, user)

        DiagramService.__prepare_to_persist(diagram, user, persisted_diagram=persisted_diagram)
        self.diagram_repository.update(diagram)

    def delete_diagram(self, diagram_id: UUID):
        user = self.authentication_repository.get_current_user()

        diagram = self.find_diagram_by_id(diagram_id, user)
        DiagramService.__prepare_to_persist(diagram, user, is_delete=True)

        self.diagram_repository.delete(diagram_id)

    def find_diagram_by_id(self, diagram_id: UUID, user: Optional[User] = None) -> Diagram:
        if not user:
            user = self.authentication_repository.get_current_user()

        diagram = self.diagram_repository.find_by_id(diagram_id)

        if not diagram:
            raise EntityNotFoundException("Diagram", diagram_id)

        if not user.allowed_to_view(diagram):
            raise PermissionException("Diagram", diagram_id, user)

        return diagram

    def find_diagrams_by_user(self) -> List[Diagram]:
        return self.diagram_repository.find_all_by_user(self.authentication_repository.get_current_user())

    @staticmethod
    def __prepare_to_persist(diagram: Diagram, user: User, is_delete: bool = False,
                             persisted_diagram: Optional[Diagram] = None):
        DiagramService.check_permission_to_persist(persisted_diagram if persisted_diagram else diagram, user,
                                                   is_delete)

        if is_delete:
            return

        diagram.set_track_data(user, datetime.now())

        if persisted_diagram:
            diagram.created_by = persisted_diagram.created_by
            diagram.created_at = persisted_diagram.created_at
        else:
            diagram.id = uuid.uuid4()

        DiagramService.__check_required_fields(diagram)

    @staticmethod
    def __check_required_fields(diagram: Diagram):
        if not diagram.name:
            raise InvalidEntityException("Diagram", ["name"])

    @staticmethod
    def check_permission_to_persist(diagram: Diagram, user: User, is_delete: bool = False):
        if not diagram.id:
            return

        # to delete an item the user must be the owner
        if is_delete and user.is_owner(diagram) or not is_delete and user.allowed_to_edit(diagram):
            return

        raise PermissionException("Diagram", diagram.id, user)
