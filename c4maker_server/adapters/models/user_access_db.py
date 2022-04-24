from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models.base_model import BaseModel
from c4maker_server.domain.entities.user_access import UserAccess, UserPermission


class UserAccessDB(BaseModel):
    __tablename__ = "user_access"
    user_id = Column(String, ForeignKey("user.id"), primary_key=True, nullable=False)
    diagram_id = Column(String, ForeignKey("diagram.id"), primary_key=True, nullable=False)
    user_permission = Column(String, primary_key=True, nullable=False)
    diagram = relationship("DiagramDB")

    def __int__(self, user_access: UserAccess, user_id: str):
        self.user_id = user_id
        self.diagram_id = user_access.diagram.id
        self.user_permission = user_access.permission.name

    def __eq__(self, other):
        return other and self.get_identifier() == other.get_identifier()

    def __hash__(self):
        return hash(self.get_identifier())

    def to_entity(self) -> UserAccess:
        return UserAccess(diagram=self.diagram.to_entity(),
                          permission=UserAccess.instantiate_permission_by_name(self.user_permission))

    def get_identifier(self) -> tuple:
        return self.user_id, self.diagram_id, self.user_permission
