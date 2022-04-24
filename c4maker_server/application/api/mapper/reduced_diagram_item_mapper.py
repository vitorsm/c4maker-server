from typing import Optional

from c4maker_server.application.api.mapper.diagram_mapper import DiagramMapper
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.utils import utils


class ReducedDiagramItemMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[DiagramItem]:
        if not dto:
            return None

        return DiagramItem(id=utils.str_to_uuid(dto.get("id")), name=dto.get("name"),
                           item_description=dto.get("item_description"), details=dto.get("details"),
                           item_type=DiagramItem.instantiate_item_type_by_name(dto.get("item_type")),
                           diagram=DiagramMapper.to_entity(dto.get("diagram")),
                           parent=ReducedDiagramItemMapper.to_entity(dto.get("parent")),
                           relationships=list())

    @staticmethod
    def to_dto(diagram_item: DiagramItem) -> Optional[dict]:
        if not diagram_item:
            return None

        dto = {
            "id": str(diagram_item.id),
            "name": diagram_item.name,
            "item_description": diagram_item.item_description,
            "details": diagram_item.details,
            "item_type": diagram_item.item_type.name,
            "diagram": DiagramMapper.to_dto(diagram_item.diagram),
            "parent": ReducedDiagramItemMapper.to_dto(diagram_item.parent),
            "relationships": None
        }

        return dto
