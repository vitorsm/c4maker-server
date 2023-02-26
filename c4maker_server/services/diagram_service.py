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
from c4maker_server.services.workspace_service import WorkspaceService


class DiagramService:
    diagram_repository: DiagramRepository

    def __init__(self, diagram_repository: DiagramRepository, authentication_repository: AuthenticationRepository,
                 workspace_service: WorkspaceService):
        self.diagram_repository = diagram_repository
        self.authentication_repository = authentication_repository
        self.workspace_service = workspace_service

    def create_diagram(self, diagram: Diagram):
        self.__prepare_to_persist(diagram, self.authentication_repository.get_current_user())
        self.diagram_repository.create(diagram)

    def update_diagram(self, diagram: Diagram):
        user = self.authentication_repository.get_current_user()
        persisted_diagram = self.find_diagram_by_id(diagram.id, user)

        self.__prepare_to_persist(diagram, user, persisted_diagram=persisted_diagram)
        self.diagram_repository.update(diagram)

    def delete_diagram(self, diagram_id: UUID):
        user = self.authentication_repository.get_current_user()

        diagram = self.find_diagram_by_id(diagram_id, user)
        self.__prepare_to_persist(diagram, user, is_delete=True)

        self.diagram_repository.delete(diagram_id)

    def find_diagram_by_id(self, diagram_id: UUID, user: Optional[User] = None) -> Diagram:
        if not user:
            user = self.authentication_repository.get_current_user()

        diagram = self.diagram_repository.find_by_id(diagram_id)

        if not diagram:
            raise EntityNotFoundException("Diagram", diagram_id)

        if not user.allowed_to_view(diagram.workspace):
            raise PermissionException("Diagram", diagram_id, user)

        return diagram

    def find_diagrams_by_workspace(self, workspace_id: UUID) -> List[Diagram]:
        self.workspace_service.find_workspace_by_id(workspace_id)
        return self.diagram_repository.find_by_workspace_id(workspace_id)

    def __prepare_to_persist(self, diagram: Diagram, user: User, is_delete: bool = False,
                             persisted_diagram: Optional[Diagram] = None):
        # this call is duplicated. Maybe there is a better idea to solve this problem
        # if we don't check this here, if we don't have a workspace it will raise an unexpected exception
        DiagramService.__check_required_fields(diagram, persisted_diagram)

        diagram.workspace = self.workspace_service.find_workspace_by_id(diagram.workspace.id, user) \
            if not persisted_diagram else persisted_diagram.workspace

        WorkspaceService.check_permission_to_persist(persisted_diagram.workspace
                                                     if persisted_diagram else diagram.workspace, user)

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
    def __check_required_fields(diagram: Diagram, persisted_diagram: Optional[Diagram] = None):
        missing_fields = list()

        if not diagram.name:
            missing_fields.append("name")

        if not diagram.diagram_type:
            missing_fields.append("diagram_type")

        if not diagram.workspace or persisted_diagram and persisted_diagram.workspace != diagram.workspace:
            missing_fields.append("workspace")

        if missing_fields:
            raise InvalidEntityException("Diagram", missing_fields)
