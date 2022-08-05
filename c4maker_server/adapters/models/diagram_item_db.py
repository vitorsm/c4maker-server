from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models import DiagramItemRelationshipDB
from c4maker_server.adapters.models.base_model import BaseModel
from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item import DiagramItem, DiagramItemType


class DiagramItemDB(BaseModel):
    __tablename__ = "diagram_item"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    item_description = Column(String, nullable=True)
    details = Column(String, nullable=True)
    item_type = Column(String(30), nullable=False, )
    diagram_id = Column(String, ForeignKey("diagram.id"), nullable=False)
    parent_id = Column(String, ForeignKey("diagram_item.id"), nullable=True)
    relationships = relationship("DiagramItemRelationshipDB",
                                 foreign_keys="DiagramItemRelationshipDB.from_diagram_item_id", lazy="select",
                                 cascade="all, delete-orphan")

    created_by = Column(String, ForeignKey("user.id"), nullable=False)
    modified_by = Column(String, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    parent = relationship("DiagramItemDB", foreign_keys="DiagramItemDB.parent_id", lazy="select", remote_side=[id])
    created_by_obj = relationship("UserDB", foreign_keys="DiagramItemDB.created_by")
    modified_by_obj = relationship("UserDB", foreign_keys="DiagramItemDB.modified_by")
    diagram = relationship("DiagramDB", lazy="select", cascade="all,delete")

    def __init__(self, diagram_item: DiagramItem):
        self.update_properties(diagram_item)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def update_properties(self, diagram_item: DiagramItem):
        self.id = str(diagram_item.id)
        self.name = diagram_item.name
        self.item_description = diagram_item.item_description
        self.details = diagram_item.details
        self.item_type = diagram_item.item_type.name
        self.diagram_id = str(diagram_item.diagram.id)
        self.parent_id = str(diagram_item.parent.id) if diagram_item.parent else None

        self.created_by = str(diagram_item.created_by.id)
        self.modified_by = str(diagram_item.modified_by.id)
        self.created_at = diagram_item.created_at
        self.modified_at = diagram_item.modified_at

        if diagram_item.relationships:
            self.relationships = [DiagramItemRelationshipDB(r, diagram_item) for r in diagram_item.relationships]

    def to_entity(self, diagram: Optional[Diagram]) -> DiagramItem:
        if not diagram:
            diagram = self.diagram.to_entity()

        relationships = [r.to_entity() for r in self.relationships]
        parent = None
        if self.parent_id:
            parent_db = self.parent[0] if isinstance(self.parent, list) else self.parent
            parent = parent_db.to_entity(diagram)

        return DiagramItem(id=UUID(self.id), name=self.name, item_description=self.item_description,
                           details=self.details, relationships=relationships, parent=parent,
                           item_type=DiagramItem.instantiate_item_type_by_name(self.item_type), diagram=diagram,
                           created_by=self.created_by_obj.to_entity(), modified_by=self.modified_by_obj.to_entity(),
                           created_at=self.created_at, modified_at=self.modified_at)
