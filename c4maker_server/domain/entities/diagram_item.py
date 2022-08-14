import enum
from dataclasses import field, dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship


class DiagramItemType(enum.Enum):
    PERSON = 1
    SOFTWARE_SYSTEM = 2
    CONTAINER = 3
    COMPONENT = 4


@dataclass
class DiagramItem:
    id: Optional[UUID]
    name: str
    item_description: str
    details: str
    item_type: DiagramItemType
    diagram: Diagram
    relationships: List[DiagramItemRelationship] = field(default=list)
    parent: Optional['DiagramItem'] = field(default=None)

    created_by: Optional = field(default=None)
    modified_by: Optional = field(default=None)
    created_at: Optional[datetime] = field(default=None)
    modified_at: Optional[datetime] = field(default=None)

    def __eq__(self, other: 'DiagramItem'):
        return isinstance(other, DiagramItem) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def set_track_data(self, user, modified_date: datetime):
        self.modified_by = user
        self.modified_at = modified_date

        if not self.created_by:
            self.created_by = user
        if not self.created_at:
            self.created_at = modified_date

    @staticmethod
    def instantiate_item_type_by_name(item_type_name: str) -> DiagramItemType:
        types = list(map(lambda t: t, DiagramItemType))
        return next((t for t in types if t.name == item_type_name), None)
