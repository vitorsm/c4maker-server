import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from c4maker_server.domain.entities.workspace import Workspace


class WorkspaceItemType(enum.Enum):
    ENTITY = 1
    PERSONA = 2
    DATABASE = 3
    CONTAINER = 4
    COMPONENT = 5


@dataclass
class WorkspaceItem:
    id: Optional[UUID]
    workspace: Workspace
    workspace_item_type: WorkspaceItemType
    key: str
    name: str
    description: str
    details: str

    created_by: Optional = field(default=None)
    modified_by: Optional = field(default=None)
    created_at: Optional[datetime] = field(default=None)
    modified_at: Optional[datetime] = field(default=None)

    @staticmethod
    def instantiate_item_type_by_name(item_type_name: str) -> WorkspaceItemType:
        types = list(map(lambda t: t, WorkspaceItemType))
        return next((t for t in types if t.name == item_type_name), None)

    def set_track_data(self, user, modified_date: datetime):
        self.modified_by = user
        self.modified_at = modified_date

        if not self.created_by:
            self.created_by = user
        if not self.created_at:
            self.created_at = modified_date
