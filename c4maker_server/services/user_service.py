import uuid

from c4maker_server.domain.entities.user import User
from c4maker_server.domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.services.ports.authentication_repository import AuthenticationRepository
from c4maker_server.services.ports.encryption_service import EncryptionService
from c4maker_server.services.ports.user_repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository, encryption_service: EncryptionService,
                 authentication_repository: AuthenticationRepository):
        self.user_repository = user_repository
        self.encryption_service = encryption_service
        self.authentication_repository = authentication_repository

    def create_user(self, user: User):
        user.id = uuid.uuid4()
        UserService.__check_required_fields(user)
        user.password = self.encryption_service.encrypt_password(user.password)

        self.user_repository.create_user(user)

    def find_current_user(self) -> User:
        return self.authentication_repository.get_current_user()

    @staticmethod
    def __check_required_fields(user: User):
        wrong_fields = list()
        if not user.name:
            wrong_fields.append("name")
        if not user.login:
            wrong_fields.append("login")
        if not user.password:
            wrong_fields.append("password")

        if wrong_fields:
            raise InvalidEntityException("User", wrong_fields)

    def authenticate(self, login: str, password: str) -> User:
        user = self.user_repository.find_by_login(login)

        if not user or not self.encryption_service.check_encrypted_password(password, user.password):
            raise InvalidCredentialsException(login)

        return user
