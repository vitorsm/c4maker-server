from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models import BaseModel
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.domain.entities.workspace_item import WorkspaceItem


class WorkspaceItemDB(BaseModel):
    __tablename__ = "workspace_item"
    id = Column(String, primary_key=True, nullable=False)
    workspace_id = Column(String, ForeignKey("workspace.id"), nullable=False)
    workspace_item_type = Column(String(30), nullable=False)
    workspace_item_key = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    details = Column(String, nullable=True)

    created_by = Column(String, ForeignKey("user.id"), nullable=False)
    modified_by = Column(String, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    created_by_obj = relationship("UserDB", foreign_keys="WorkspaceItemDB.created_by")
    modified_by_obj = relationship("UserDB", foreign_keys="WorkspaceItemDB.modified_by")

    workspace = relationship("WorkspaceDB", lazy="select", cascade="all,delete")

    def __init__(self, workspace_item: WorkspaceItem):
        self.update_properties(workspace_item)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def update_properties(self, workspace_item: WorkspaceItem):
        self.id = str(workspace_item.id)
        self.workspace_id = str(workspace_item.workspace.id)
        self.workspace_item_type = workspace_item.workspace_item_type.name
        self.workspace_item_key = workspace_item.key
        self.name = workspace_item.name
        self.description = workspace_item.description
        self.details = workspace_item.details

        self.created_at = workspace_item.created_at
        self.modified_at = workspace_item.modified_at
        self.created_by = str(workspace_item.created_by.id)
        self.modified_by = str(workspace_item.modified_by.id)

    def to_entity(self, workspace: Optional[Workspace] = None) -> WorkspaceItem:
        if not workspace:
            workspace = self.workspace.to_entity()

        return WorkspaceItem(id=UUID(self.id), workspace=workspace,
                             workspace_item_type=WorkspaceItem.instantiate_item_type_by_name(self.workspace_item_type),
                             key=self.workspace_item_key, name=self.name, description=self.description,
                             details=self.details, created_at=self.created_at, modified_at=self.modified_at,
                             created_by=self.created_by_obj.to_entity(), modified_by=self.modified_by_obj.to_entity())
