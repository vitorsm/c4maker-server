from sqlalchemy import Column, String, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship

from c4maker_server.adapters.mapper.diagram_item_relationship_mapper import DiagramItemRelationshipMapper
from c4maker_server.adapters.models.base_model import BaseModel
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship


class DiagramItemRelationshipDB(BaseModel):
    __tablename__ = "diagram_item_relationship"
    from_diagram_item_id = Column(String, ForeignKey("diagram_item.id"), primary_key=True, nullable=False)
    to_diagram_item_id = Column(String, ForeignKey("diagram_item.id"), primary_key=True, nullable=False)
    description = Column(String, primary_key=True, nullable=False)
    details = Column(String, nullable=True)
    data = Column(JSON, nullable=True)
    diagram_type = Column(Integer)

    to_diagram_item = relationship("DiagramItemDB", foreign_keys="DiagramItemRelationshipDB.to_diagram_item_id")

    def __init__(self, diagram_item_relationship: DiagramItemRelationship, diagram_item: DiagramItem):
        self.from_diagram_item_id = str(diagram_item.id)
        self.to_diagram_item_id = str(diagram_item_relationship.diagram_item.id)
        self.description = diagram_item_relationship.description
        self.details = diagram_item_relationship.details
        self.data = DiagramItemRelationshipMapper.entity_to_db(diagram_item_relationship)
        self.diagram_type = diagram_item_relationship.DIAGRAM_ITEM_TYPE.value

    def __eq__(self, other):
        return other and self.get_identifier() == other.get_identifier()

    def __hash__(self):
        return hash(self.get_identifier())

    def to_entity(self) -> DiagramItemRelationship:
        item_relationship = DiagramItemRelationship(diagram_item=self.to_diagram_item.to_entity(None),
                                                    description=self.description, details=self.details)

        return DiagramItemRelationshipMapper.db_to_entity(item_relationship, self.data, self.diagram_type)

    def get_identifier(self) -> tuple:
        return self.from_diagram_item_id, self.to_diagram_item_id, self.description
