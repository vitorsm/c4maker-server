from dataclasses import dataclass


@dataclass
class DiagramItemRelationship:
    diagram_item: 'DiagramItem'
    description: str
    details: str
