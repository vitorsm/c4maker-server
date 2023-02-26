import enum
from dataclasses import field, dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship
from c4maker_server.domain.entities.workspace_item import WorkspaceItem


@dataclass
class DiagramItem:
    id: Optional[UUID]
    workspace_item: WorkspaceItem
    diagram: Diagram
    relationships: List[DiagramItemRelationship] = field(default=list)
    parent: Optional['DiagramItem'] = field(default=None)

    def __eq__(self, other: 'DiagramItem'):
        return isinstance(other, DiagramItem) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
