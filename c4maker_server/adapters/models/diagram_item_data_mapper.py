from typing import Tuple, Optional

from c4maker_server.domain.entities.c4_diagram_item import C4DiagramItem, ItemPosition
from c4maker_server.domain.entities.diagram import DiagramType
from c4maker_server.domain.entities.diagram_item import DiagramItem


class DiagramItemDataMapper:

    @staticmethod
    def entity_to_db(diagram_item: DiagramItem) -> Tuple[dict, int]:
        if isinstance(diagram_item, C4DiagramItem):
            return DiagramItemDataMapper.c4_item_to_db(diagram_item)

        raise ValueError("Invalid diagram item")

    @staticmethod
    def db_to_entity(diagram_item: DiagramItem, data: dict, diagram_item_type: int) -> DiagramItem:
        if diagram_item_type == DiagramType.C4.value:
            return DiagramItemDataMapper.db_to_c4(diagram_item, data)

        raise ValueError("Invalid diagram item type %s", diagram_item_type)

    @staticmethod
    def db_to_c4(diagram_item: DiagramItem, data: Optional[dict]) -> C4DiagramItem:
        position = None
        position_dto = data.get("position") if data else None
        if position_dto:
            position = ItemPosition(x=position_dto.get("x"), y=position_dto.get("y"), width=position_dto.get("width"),
                                    height=position_dto.get("height"))

        c4_item = C4DiagramItem(id=diagram_item.id, workspace_item=diagram_item.workspace_item,
                                diagram=diagram_item.diagram, relationships=diagram_item.relationships)
        c4_item.position = position
        c4_item.color = data.get("color") if data else None

        return c4_item

    @staticmethod
    def c4_item_to_db(diagram_item: C4DiagramItem) -> Tuple[dict, int]:
        position = None
        if diagram_item.position:
            position = {
                "x": diagram_item.position.x,
                "y": diagram_item.position.y,
                "width": diagram_item.position.width,
                "height": diagram_item.position.height
            }

        data = {
            "position": position,
            "color": diagram_item.color
        }

        return data, DiagramType.C4.value
