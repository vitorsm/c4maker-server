import abc
from typing import Optional

from c4maker_server.domain.entities.user import User


class UserRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_login(self, login: str) -> Optional[User]:
        raise NotImplementedError
