from uuid import UUID

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from c4maker_server.adapters.models import UserAccessDB
from c4maker_server.adapters.models.base_model import BaseModel
from c4maker_server.domain.entities.user import User


class UserDB(BaseModel):
    __tablename__ = "user"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_access = relationship("UserAccessDB", lazy="select")

    def __init__(self, user: User):
        self.id = str(user.id)
        self.name = user.name
        self.login = user.login
        self.password = user.password
        if user.user_access:
            self.user_access = [UserAccessDB(u) for u in user.user_access]

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def to_entity(self, reduced: bool = True) -> User:
        user_access = list()
        if not reduced:
            user_access = [u.to_entity() for u in self.user_access]

        return User(id=UUID(self.id), name=self.name, login=self.login, password=self.password,
                    user_access=user_access)
