from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models.base_model import BaseModel
from c4maker_server.domain.entities.user_access import UserAccess


class UserAccessDB(BaseModel):
    __tablename__ = "user_access"
    user_id = Column(String, ForeignKey("user.id"), primary_key=True, nullable=False)
    workspace_id = Column(String, ForeignKey("workspace.id"), primary_key=True, nullable=False)
    user_permission = Column(String, primary_key=True, nullable=False)
    workspace = relationship("WorkspaceDB")

    def __int__(self, user_access: UserAccess, user_id: str):
        self.user_id = user_id
        self.workspace_id = user_access.workspace.id
        self.user_permission = user_access.permission.name

    def __eq__(self, other):
        return other and self.get_identifier() == other.get_identifier()

    def __hash__(self):
        return hash(self.get_identifier())

    def to_entity(self) -> UserAccess:
        return UserAccess(workspace=self.workspace.to_entity(),
                          permission=UserAccess.instantiate_permission_by_name(self.user_permission))

    def get_identifier(self) -> tuple:
        return self.user_id, self.workspace_id, self.user_permission
