from c4maker_server.domain.entities.diagram import DiagramType
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.entities.item_position import ItemPosition


class C4DiagramItem(DiagramItem):
    DIAGRAM_ITEM_TYPE = DiagramType.C4
    position: ItemPosition
    color: str
