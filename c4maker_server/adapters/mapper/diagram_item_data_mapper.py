from typing import Tuple, Optional

from c4maker_server.adapters.mapper.item_position_mapper import ItemPositionMapper
from c4maker_server.domain.entities.c4_diagram_item import C4DiagramItem, ItemPosition
from c4maker_server.domain.entities.diagram import DiagramType
from c4maker_server.domain.entities.diagram_item import DiagramItem


class DiagramItemDataMapper:

    @staticmethod
    def entity_to_db(diagram_item: DiagramItem) -> Tuple[dict, int]:
        if isinstance(diagram_item, C4DiagramItem):
            return DiagramItemDataMapper.__c4_item_to_db(diagram_item)

        raise ValueError("Invalid diagram item %", type(diagram_item))

    @staticmethod
    def db_to_entity(diagram_item: DiagramItem, data: dict, diagram_item_type: int) -> DiagramItem:
        if diagram_item_type == DiagramType.C4.value:
            return DiagramItemDataMapper.__db_to_c4(diagram_item, data)

        raise ValueError("Invalid diagram item type %s", diagram_item_type)

    @staticmethod
    def __db_to_c4(diagram_item: DiagramItem, data: Optional[dict]) -> C4DiagramItem:
        c4_item = C4DiagramItem(id=diagram_item.id, workspace_item=diagram_item.workspace_item,
                                diagram=diagram_item.diagram, relationships=diagram_item.relationships,
                                parent=diagram_item.parent)
        c4_item.position = ItemPositionMapper.db_to_entity(data.get("position"))
        c4_item.color = data.get("color") if data else None

        return c4_item

    @staticmethod
    def __c4_item_to_db(diagram_item: C4DiagramItem) -> Tuple[dict, int]:
        data = {
            "position": ItemPositionMapper.entity_to_db(diagram_item.position),
            "color": diagram_item.color
        }

        return data, DiagramType.C4.value
