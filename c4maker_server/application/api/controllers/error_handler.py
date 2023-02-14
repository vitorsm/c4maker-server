from flask_jwt import JWTError

# from c4maker_server.application.api import namespace
from c4maker_server.application.api.controllers import namespace
from c4maker_server.domain.exceptions.duplicate_entity_exception import DuplicateEntityException
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException


@namespace.errorhandler(DuplicateEntityException)
def duplicate_entity_error(ex: DuplicateEntityException):
    return {'message': str(ex)}, 409


@namespace.errorhandler(JWTError)
def jwt_required_error(ex: JWTError):
    return {'message': str(ex)}, ex.status_code


@namespace.errorhandler(EntityNotFoundException)
def jwt_required_error(ex: EntityNotFoundException):
    return {'message': str(ex)}, 404


@namespace.errorhandler(InvalidEntityException)
def jwt_required_error(ex: InvalidEntityException):
    return {'message': str(ex)}, 400


@namespace.errorhandler(PermissionException)
def jwt_required_error(ex: PermissionException):
    return {'message': str(ex)}, 403
