from typing import Optional

from c4maker_server.application.api.mapper.diagram_item_relationship_mapper import DiagramItemRelationshipMapper
from c4maker_server.application.api.mapper.reduced_diagram_item_mapper import ReducedDiagramItemMapper
from c4maker_server.domain.entities.diagram_item import DiagramItem


class DiagramItemMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[DiagramItem]:
        if not dto:
            return None

        diagram_item = ReducedDiagramItemMapper.to_entity(dto)
        diagram_item.relationships = [DiagramItemRelationshipMapper.to_entity(r) for r in dto.get("relationships", [])]

        return diagram_item

    @staticmethod
    def to_dto(diagram_item: DiagramItem) -> Optional[dict]:
        if not diagram_item:
            return None

        dto = ReducedDiagramItemMapper.to_dto(diagram_item)
        dto["relationships"] = [DiagramItemRelationshipMapper.to_dto(r) for r in diagram_item.relationships]

        return dto
