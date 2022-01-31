from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Diagram:
    id: Optional[UUID]
    name: str
    description: Optional[str]

    created_by: Optional = field(default=None)
    modified_by: Optional = field(default=None)
    created_at: Optional[datetime] = field(default=None)
    modified_at: Optional[datetime] = field(default=None)

    def __eq__(self, other: 'Diagram'):
        return isinstance(other, Diagram) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def set_track_data(self, user, modified_date: datetime):
        self.modified_by = user
        self.modified_at = modified_date

        if not self.created_by:
            self.created_by = user
        if not self.created_at:
            self.created_at = modified_date
