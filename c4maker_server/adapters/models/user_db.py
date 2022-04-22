from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models.base_model import BaseModel


class UserDB(BaseModel):
    __tablename__ = "user"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_access = relationship("UserAccessDB", lazy="select", cascade="all, delete-orphan")

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
