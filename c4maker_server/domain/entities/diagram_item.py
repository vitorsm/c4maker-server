import enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship
from c4maker_server.domain.entities.user import User


class DiagramItemType(enum.Enum):
    PERSON = 1
    SOFTWARE_SYSTEM = 2
    CONTAINER = 3
    COMPONENT = 4


@dataclass
class DiagramItem:
    id: UUID
    name: str
    item_description: str
    details: str
    item_type: DiagramItemType
    relationships: List[DiagramItemRelationship]
    parent: Optional['DiagramItem']
    diagram: Diagram

    created_by: User
    modified_by: User
    created_at: datetime
    modified_at: datetime

    def __eq__(self, other: 'DiagramItem'):
        return isinstance(other, DiagramItem) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def set_track_data(self, user: User, modified_date: datetime):
        self.modified_by = user
        self.modified_at = modified_date

        if not self.modified_by:
            self.modified_by = user
        if not self.modified_at:
            self.modified_at = modified_date
