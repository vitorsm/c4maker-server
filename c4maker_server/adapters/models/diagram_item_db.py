from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models import DiagramItemRelationshipDB
from c4maker_server.adapters.models.base_model import BaseModel
from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item import DiagramItem


class DiagramItemDB(BaseModel):
    __tablename__ = "diagram_item"
    id = Column(String, primary_key=True, nullable=False)
    diagram_id = Column(String, ForeignKey("diagram.id"), nullable=False)
    parent_id = Column(String, ForeignKey("diagram_item.id"), nullable=True)
    workspace_item_id = Column(String, ForeignKey("workspace_item.id"), nullable=False)

    relationships = relationship("DiagramItemRelationshipDB",
                                 foreign_keys="DiagramItemRelationshipDB.from_diagram_item_id", lazy="select",
                                 cascade="all, delete-orphan")

    workspace_item_obj = relationship("WorkspaceItemDB", foreign_keys="DiagramItemDB.workspace_item_id")
    parent = relationship("DiagramItemDB", foreign_keys="DiagramItemDB.parent_id", lazy="select", remote_side=[id])
    diagram = relationship("DiagramDB", lazy="select", cascade="all,delete")

    def __init__(self, diagram_item: DiagramItem):
        self.update_properties(diagram_item)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def update_properties(self, diagram_item: DiagramItem):
        self.id = str(diagram_item.id)
        self.diagram_id = str(diagram_item.diagram.id)
        self.parent_id = str(diagram_item.parent.id) if diagram_item.parent else None
        self.workspace_item_id = str(diagram_item.workspace_item.id)

        if not diagram_item.relationships:
            self.relationships = list()
        else:
            self.relationships = [DiagramItemRelationshipDB(r, diagram_item) for r in diagram_item.relationships]

    def to_entity(self, diagram: Optional[Diagram]) -> DiagramItem:
        if not diagram:
            diagram = self.diagram.to_entity()

        relationships = [r.to_entity() for r in self.relationships]
        parent = None
        if self.parent_id:
            parent_db = self.parent[0] if isinstance(self.parent, list) else self.parent
            parent = parent_db.to_entity(diagram)

        workspace_item = None
        if self.workspace_item_id:
            workspace_item_db = self.workspace_item_obj[0] if isinstance(self.workspace_item_obj, list) else \
                self.workspace_item_obj
            workspace_item = workspace_item_db.to_entity(diagram.workspace)

        return DiagramItem(id=UUID(self.id), workspace_item=workspace_item, relationships=relationships, parent=parent,
                           diagram=diagram)
