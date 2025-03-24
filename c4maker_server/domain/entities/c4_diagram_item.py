from dataclasses import dataclass

from c4maker_server.domain.entities.diagram_item import DiagramItem


@dataclass
class ItemPosition:
    x: float
    y: float
    width: float
    height: float

class C4DiagramItem(DiagramItem):
    position: ItemPosition
    color: str
