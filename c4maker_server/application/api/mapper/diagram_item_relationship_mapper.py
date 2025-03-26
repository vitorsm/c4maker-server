from typing import Optional

from c4maker_server.application.api.mapper.item_position_mapper import ItemPositionMapper
from c4maker_server.application.api.mapper.reduced_diagram_item_mapper import ReducedDiagramItemMapper
from c4maker_server.domain.entities.c4_diagram_item_relationship import C4DiagramItemRelationship
from c4maker_server.domain.entities.diagram import Diagram, DiagramType
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException


class DiagramItemRelationshipMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[DiagramItemRelationship]:
        if not dto:
            return None

        diagram_type = Diagram.instantiate_diagram_type_by_name(dto.get("diagram_type"))

        relationship = DiagramItemRelationship(diagram_item=ReducedDiagramItemMapper.to_entity(dto.get("diagram_item")),
                                               description=dto.get("description"), details=dto.get("details"))

        if diagram_type == DiagramType.C4:
            return DiagramItemRelationshipMapper.__to_c4_entity(relationship, dto)

        raise InvalidEntityException("DiagramItemRelationship", ["diagram_type"])

    @staticmethod
    def to_dto(diagram_item_relationship: DiagramItemRelationship) -> Optional[dict]:
        if not diagram_item_relationship:
            return None

        dto = {
            "diagram_item": ReducedDiagramItemMapper.to_dto(diagram_item_relationship.diagram_item),
            "description": diagram_item_relationship.description,
            "details": diagram_item_relationship.details
        }

        if isinstance(diagram_item_relationship, C4DiagramItemRelationship):
            return DiagramItemRelationshipMapper.__to_c4_dto(diagram_item_relationship, dto)

        raise InvalidEntityException("DiagramItemRelationship", ["diagram_type"])

    @staticmethod
    def __to_c4_dto(relationship: C4DiagramItemRelationship, dto: dict) -> dict:
        dto["diagram_type"] = relationship.DIAGRAM_ITEM_TYPE.name

        dto["data"] = {
            "from_position": ItemPositionMapper.to_dto(relationship.from_position),
            "to_position": ItemPositionMapper.to_dto(relationship.to_position)
        }

        return dto

    @staticmethod
    def __to_c4_entity(relationship: DiagramItemRelationship, dto: dict) -> C4DiagramItemRelationship:
        c4_relationship = C4DiagramItemRelationship(diagram_item=relationship.diagram_item,
                                                    description=relationship.description, details=relationship.details)

        item_data = dto.get("data")
        c4_relationship.from_position = ItemPositionMapper.to_entity(item_data.get("from_position"))
        c4_relationship.to_position = ItemPositionMapper.to_entity(item_data.get("to_position"))

        return c4_relationship
