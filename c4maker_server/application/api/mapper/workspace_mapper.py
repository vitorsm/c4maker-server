from typing import Optional

from c4maker_server.application.api.mapper.diagram_mapper import DiagramMapper
from c4maker_server.application.api.mapper.generic_mapper import GenericMapper
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.utils import utils


class WorkspaceMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[Workspace]:
        if not dto:
            return None

        return Workspace(id=utils.str_to_uuid(dto.get("id")), name=dto.get("name"), description=dto.get("description"),
                         diagrams=list())

    @staticmethod
    def to_dto(workspace: Workspace) -> Optional[dict]:
        if not workspace:
            return None

        dto = {
            "id": str(workspace.id),
            "name": workspace.name,
            "description": workspace.description,
            "diagrams": [DiagramMapper.to_dto(diagram) for diagram in workspace.diagrams] if workspace.diagrams else []
        }

        GenericMapper.to_dto(workspace, dto)

        return dto
