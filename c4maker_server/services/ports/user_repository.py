import abc
from typing import Optional
from uuid import UUID

from c4maker_server.domain.entities.user import User


class UserRepository(metaclass=abc.ABCMeta):

    def create_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, user_id: UUID, reduced: bool = True) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_login(self, login: str) -> Optional[User]:
        raise NotImplementedError
