from sqlalchemy import Column, String, ForeignKey

from c4maker_server.adapters.models.base_model import BaseModel


class DiagramItemRelationshipDB(BaseModel):
    __tablename__ = "diagram_item_relationship"
    from_diagram_item_id = Column(String, ForeignKey("diagram_item.id"), primary_key=True, nullable=False)
    to_diagram_item_id = Column(String, ForeignKey("diagram_item.id"), primary_key=True, nullable=False)
    description = Column(String, primary_key=True, nullable=False)
    details = Column(String, nullable=True)

    def get_identifier(self) -> tuple:
        return self.from_diagram_item_id, self.to_diagram_item_id, self.description

    def __eq__(self, other):
        return other and self.get_identifier() == other.get_identifier()

    def __hash__(self):
        return hash(self.get_identifier())
