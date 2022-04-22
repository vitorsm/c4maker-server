from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models.base_model import BaseModel


class DiagramItemDB(BaseModel):
    __tablename__ = "diagram_item"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    item_description = Column(String, nullable=True)
    details = Column(String, nullable=True)
    item_type = Column(String, nullable=False)
    diagram_id = Column(String, ForeignKey("diagram.id"), nullable=False)
    parent_id = Column(String, ForeignKey("diagram_item.id"), nullable=False)
    relationships = relationship("DiagramItemRelationshipDB",
                                 foreign_keys="DiagramItemRelationshipDB.from_diagram_item_id", lazy="select",
                                 cascade="all, delete-orphan")

    created_by = Column(String, ForeignKey("user.id"), nullable=False)
    modified_by = Column(String, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
