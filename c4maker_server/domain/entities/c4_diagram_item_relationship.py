from c4maker_server.domain.entities.diagram import DiagramType
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship
from c4maker_server.domain.entities.item_position import ItemPosition


class C4DiagramItemRelationship(DiagramItemRelationship):
    DIAGRAM_ITEM_TYPE = DiagramType.C4
    from_position: ItemPosition
    to_position: ItemPosition
