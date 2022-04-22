from sqlalchemy import Column, String, ForeignKey

from c4maker_server.adapters.models.base_model import BaseModel


class UserAccessDB(BaseModel):
    __tablename__ = "user_access"
    user_id = Column(String, ForeignKey("user.id"), primary_key=True, nullable=False)
    diagram_id = Column(String, ForeignKey("diagram.id"), primary_key=True, nullable=False)
    user_permission = Column(String, primary_key=True, nullable=False)

    def get_identifier(self) -> tuple:
        return self.user_id, self.diagram_id, self.user_permission

    def __eq__(self, other):
        return other and self.get_identifier() == other.get_identifier()

    def __hash__(self):
        return hash(self.get_identifier())
