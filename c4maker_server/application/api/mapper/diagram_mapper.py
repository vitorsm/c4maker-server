from typing import Optional

from c4maker_server.application.api.mapper.generic_mapper import GenericMapper
from c4maker_server.application.api.mapper.reduced_workspace_mapper import ReducedWorkspaceMapper
from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.utils import utils


class DiagramMapper:

    @staticmethod
    def to_entity(diagram_dto: dict) -> Optional[Diagram]:
        if not diagram_dto:
            return None

        return Diagram(id=utils.str_to_uuid(diagram_dto.get("id")), name=diagram_dto.get("name"),
                       description=diagram_dto.get("description"),
                       workspace=ReducedWorkspaceMapper.to_entity(diagram_dto.get("workspace")),
                       diagram_type=Diagram.instantiate_diagram_type_by_name(diagram_dto.get("diagram_type")))

    @staticmethod
    def to_dto(diagram: Diagram) -> Optional[dict]:
        if not diagram:
            return None

        dto = {
            "id": str(diagram.id),
            "name": diagram.name,
            "description": diagram.description,
            "diagram_type": diagram.diagram_type.name,
            "workspace": ReducedWorkspaceMapper.to_dto(diagram.workspace)
        }

        GenericMapper.to_dto(diagram, dto)

        return dto
