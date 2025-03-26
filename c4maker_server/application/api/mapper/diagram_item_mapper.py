from typing import Optional

from c4maker_server.application.api.mapper.diagram_item_relationship_mapper import DiagramItemRelationshipMapper
from c4maker_server.application.api.mapper.item_position_mapper import ItemPositionMapper
from c4maker_server.application.api.mapper.reduced_diagram_item_mapper import ReducedDiagramItemMapper
from c4maker_server.domain.entities.c4_diagram_item import C4DiagramItem, ItemPosition
from c4maker_server.domain.entities.diagram import Diagram, DiagramType
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException


class DiagramItemMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[DiagramItem]:
        if not dto:
            return None

        diagram_item = ReducedDiagramItemMapper.to_entity(dto)
        diagram_item.relationships = [DiagramItemRelationshipMapper.to_entity(r) for r in dto.get("relationships", [])]

        diagram_item_type = Diagram.instantiate_diagram_type_by_name(dto.get("diagram_item_type"))

        if diagram_item_type == DiagramType.C4:
            return DiagramItemMapper.__to_c4_entity(diagram_item, dto)

        raise InvalidEntityException("DiagramItem", ['diagram_item_type'])

    @staticmethod
    def to_dto(diagram_item: DiagramItem) -> Optional[dict]:
        if not diagram_item:
            return None

        dto = ReducedDiagramItemMapper.to_dto(diagram_item)
        dto["relationships"] = [DiagramItemRelationshipMapper.to_dto(r) for r in diagram_item.relationships]

        if isinstance(diagram_item, C4DiagramItem):
            return DiagramItemMapper.__to_c4_dto(diagram_item, dto)

        raise InvalidEntityException("DiagramItem", ["diagram_item_type"])

    @staticmethod
    def __to_c4_dto(diagram_item: C4DiagramItem, dto: dict) -> dict:
        dto["diagram_item_type"] = DiagramType.C4.name

        dto["data"] = {
            "position": ItemPositionMapper.to_dto(diagram_item.position),
            "color": diagram_item.color
        }

        return dto

    @staticmethod
    def __to_c4_entity(diagram_item: DiagramItem, dto: dict) -> C4DiagramItem:
        c4_item = C4DiagramItem(id=diagram_item.id, workspace_item=diagram_item.workspace_item,
                                diagram=diagram_item.diagram, relationships=diagram_item.relationships,
                                parent=diagram_item.parent)

        item_data = dto.get("data")

        c4_item.position = ItemPositionMapper.to_entity(item_data.get("position"))
        c4_item.color = item_data.get("color")

        return c4_item
