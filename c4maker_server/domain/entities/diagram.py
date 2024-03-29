import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from c4maker_server.domain.entities.workspace import Workspace


class DiagramType(enum.Enum):
    C4 = 1
    SEQUENCE = 2
    TEXT = 3


@dataclass
class Diagram:
    id: Optional[UUID]
    name: str
    description: Optional[str]
    workspace: Workspace
    diagram_type: DiagramType

    created_by: Optional = field(default=None)
    modified_by: Optional = field(default=None)
    created_at: Optional[datetime] = field(default=None)
    modified_at: Optional[datetime] = field(default=None)

    def __eq__(self, other: 'Diagram'):
        return isinstance(other, Diagram) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def instantiate_diagram_type_by_name(diagram_type_name: str) -> DiagramType:
        types = list(map(lambda t: t, DiagramType))
        return next((t for t in types if t.name == diagram_type_name), None)

    def set_track_data(self, user, modified_date: datetime):
        self.modified_by = user
        self.modified_at = modified_date

        if not self.created_by:
            self.created_by = user
        if not self.created_at:
            self.created_at = modified_date
