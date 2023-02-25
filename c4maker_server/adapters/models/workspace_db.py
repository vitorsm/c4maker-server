from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models.base_model import BaseModel
from c4maker_server.domain.entities.workspace import Workspace


class WorkspaceDB(BaseModel):
    __tablename__ = "workspace"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    created_by = Column(String, ForeignKey("user.id"), nullable=False)
    modified_by = Column(String, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    created_by_obj = relationship("UserDB", foreign_keys="DiagramDB.created_by")
    modified_by_obj = relationship("UserDB", foreign_keys="DiagramDB.modified_by")
    diagrams = relationship("DiagramDB", lazy="select", cascade="delete")
    workspace_items = relationship("WorkspaceItemDB", lazy="select", cascade="delete")
    user_accesses = relationship("UserAccessDB", lazy="select", cascade="delete")

    def __init__(self, workspace: Workspace):
        self.update_properties(workspace)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def update_properties(self, workspace: Workspace):
        self.id = str(workspace.id)
        self.name = workspace.name
        self.description = workspace.description

        self.created_by = str(workspace.created_by.id)
        self.modified_by = str(workspace.modified_by.id)
        self.created_at = workspace.created_at
        self.modified_at = workspace.modified_at

    def to_entity(self) -> Workspace:
        return Workspace(id=UUID(self.id), name=self.name, description=self.description,
                         created_by=self.created_by_obj.to_entity(), modified_by=self.modified_by_obj.to_entity(),
                         created_at=self.created_at, modified_at=self.modified_at)
