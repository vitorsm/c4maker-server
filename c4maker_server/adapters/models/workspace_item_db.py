from typing import Optional
from uuid import UUID

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models import BaseModel
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.domain.entities.workspace_item import WorkspaceItem


class WorkspaceItemDB(BaseModel):
    __tablename__ = "workspace_item"
    id = Column(String, primary_key=True, nullable=False)
    workspace_id = Column(String, ForeignKey("workspace.id"), nullable=False)
    workspace_item_type = Column(String(30), nullable=False, )
    key = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    details = Column(String, nullable=False)

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
        self.key = workspace_item.key
        self.name = workspace_item.name
        self.description = workspace_item.description
        self.details = workspace_item.details

    def to_entity(self, workspace: Optional[Workspace] = None) -> WorkspaceItem:
        if not workspace:
            workspace = self.workspace.to_entity()

        return WorkspaceItem(id=UUID(self.id), workspace=workspace,
                             workspace_item_type=WorkspaceItem.instantiate_item_type_by_name(self.workspace_item_type),
                             key=self.key, name=self.name, description=self.description, details=self.details)
