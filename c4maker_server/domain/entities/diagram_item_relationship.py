from dataclasses import dataclass

from c4maker_server.domain.entities.diagram import DiagramType


@dataclass
class DiagramItemRelationship:
    DIAGRAM_ITEM_TYPE = None
    diagram_item: 'DiagramItem'
    description: str
    details: str
