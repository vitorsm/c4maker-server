from typing import Optional

from c4maker_server.application.api.mapper.reduced_diagram_item_mapper import ReducedDiagramItemMapper
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship


class DiagramItemRelationshipMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[DiagramItemRelationship]:
        if not dto:
            return None

        return DiagramItemRelationship(diagram_item=ReducedDiagramItemMapper.to_entity(dto.get("diagram_item")),
                                       description=dto.get("description"), details=dto.get("details"))

    @staticmethod
    def to_dto(diagram_item_relationship: DiagramItemRelationship) -> Optional[dict]:
        if not diagram_item_relationship:
            return None

        return {
            "diagram_item": ReducedDiagramItemMapper.to_dto(diagram_item_relationship.diagram_item),
            "description": diagram_item_relationship.description,
            "details": diagram_item_relationship.details
        }
