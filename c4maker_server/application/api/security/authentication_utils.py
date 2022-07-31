from flask import Flask
from flask_jwt import JWT, JWTError
from injector import Injector

from c4maker_server.application.api.security.auth_user import AuthUser
from c4maker_server.domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from c4maker_server.services.ports.user_repository import UserRepository
from c4maker_server.services.user_service import UserService
from c4maker_server.utils import utils


def fill_jwt_auth_function(app: Flask, injector: Injector) -> JWT:

    def authenticate(login: str, password: str):
        user_service = injector.get(UserService)

        try:
            return AuthUser(user_service.authenticate(login, password))
        except InvalidCredentialsException as ex:
            raise JWTError("Invalid credentials", str(ex))

    def identity(payload: dict):
        user_repository = injector.get(UserRepository)
        user_id = utils.str_to_uuid(payload.get("identity"))
        return user_repository.find_by_id(user_id, reduced=False)

    return JWT(app, authenticate, identity)
