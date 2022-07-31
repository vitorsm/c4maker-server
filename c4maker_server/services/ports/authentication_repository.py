import abc

from c4maker_server.domain.entities.user import User


class AuthenticationRepository(metaclass=abc.ABCMeta):

    def get_current_user(self) -> User:
        raise NotImplementedError
