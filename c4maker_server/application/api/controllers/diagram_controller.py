from flask import request
from flask_jwt import jwt_required
from flask_restx import Resource

from c4maker_server.application.api import namespace, diagram_model, dependency_injector
from c4maker_server.application.api.mapper.diagram_mapper import DiagramMapper
from c4maker_server.services.diagram_service import DiagramService


@namespace.route("/diagram")
class DiagramController(Resource):

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.expect(diagram_model, validate=True)
    @namespace.marshal_with(diagram_model)
    def post(self):
        payload = request.get_json()
        diagram = DiagramMapper.to_entity(payload)
        dependency_injector.get(DiagramService).create_diagram(diagram)

        return DiagramMapper.to_dto(diagram), 201
