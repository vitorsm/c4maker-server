from flask import request
from flask_restx import Resource

# from c4maker_server.application.api import namespace, user_model, dependency_injector
from c4maker_server.application.api.controllers import namespace, user_model, dependency_injector
from c4maker_server.application.api.mapper.user_mapper import UserMapper
from c4maker_server.services.user_service import UserService


@namespace.route("/user")
class UserController(Resource):

    @namespace.expect(user_model, validate=True)
    @namespace.marshal_with(user_model)
    def post(self):
        payload = request.get_json()
        user = UserMapper.to_entity(payload)
        dependency_injector.get(UserService).create_user(user)

        return UserMapper.to_dto(user), 201
