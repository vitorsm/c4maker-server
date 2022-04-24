from c4maker_server.domain.entities.user import User
from c4maker_server.domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from c4maker_server.services.ports.encryption_service import EncryptionService
from c4maker_server.services.ports.user_repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository, encryption_service: EncryptionService):
        self.user_repository = user_repository
        self.encryption_service = encryption_service

    def authenticate(self, login: str, password: str) -> User:
        user = self.user_repository.find_by_login(login)

        if not user or not self.encryption_service.check_encrypted_password(password, user.password):
            raise InvalidCredentialsException(login)

        return user
