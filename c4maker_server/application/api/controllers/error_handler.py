from flask_jwt import JWTError

from c4maker_server.application.api import namespace


@namespace.errorhandler(JWTError)
def jwt_required_error(ex: JWTError):
    return {'message': str(ex)}, ex.status_code
