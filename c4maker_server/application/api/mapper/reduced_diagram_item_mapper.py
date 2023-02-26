from typing import Optional

from c4maker_server.application.api.mapper.diagram_mapper import DiagramMapper
from c4maker_server.application.api.mapper.generic_mapper import GenericMapper
from c4maker_server.application.api.mapper.workspace_item_mapper import WorkspaceItemMapper
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.utils import utils


class ReducedDiagramItemMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[DiagramItem]:
        if not dto:
            return None

        return DiagramItem(id=utils.str_to_uuid(dto.get("id")),
                           workspace_item=WorkspaceItemMapper.to_entity(dto.get("workspace_item")),
                           diagram=DiagramMapper.to_entity(dto.get("diagram")),
                           parent=ReducedDiagramItemMapper.to_entity(dto.get("parent")),
                           relationships=list())

    @staticmethod
    def to_dto(diagram_item: DiagramItem) -> Optional[dict]:
        if not diagram_item:
            return None

        dto = {
            "id": str(diagram_item.id),
            "workspace_item": WorkspaceItemMapper.to_dto(diagram_item.workspace_item),
            "diagram": DiagramMapper.to_dto(diagram_item.diagram),
            "parent": ReducedDiagramItemMapper.to_dto(diagram_item.parent),
            "relationships": None
        }

        GenericMapper.to_dto(diagram_item, dto)

        return dto
