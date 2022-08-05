from flask import request
from flask_jwt import jwt_required
from flask_restx import Resource

# from c4maker_server.application.api import namespace, diagram_model, dependency_injector
from c4maker_server.application.api.controllers import namespace, diagram_model, dependency_injector
from c4maker_server.application.api.mapper.diagram_mapper import DiagramMapper
from c4maker_server.services.diagram_service import DiagramService
from c4maker_server.utils import utils


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

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(diagram_model)
    def get(self):
        diagrams = dependency_injector.get(DiagramService).find_diagrams_by_user()
        return [DiagramMapper.to_dto(diagram) for diagram in diagrams]


@namespace.route("/diagram/<string:diagram_item_id>")
class DiagramItemController(Resource):

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.expect(diagram_model, validate=True)
    @namespace.marshal_with(diagram_model)
    def put(self, diagram_item_id: str):
        payload = request.get_json()
        diagram = DiagramMapper.to_entity(payload)
        diagram.id = utils.str_to_uuid(diagram_item_id)
        dependency_injector.get(DiagramService).update_diagram(diagram)

        return DiagramMapper.to_dto(diagram)

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(diagram_model)
    def get(self, diagram_item_id: str):
        diagram = dependency_injector.get(DiagramService).find_diagram_by_id(utils.str_to_uuid(diagram_item_id))

        return DiagramMapper.to_dto(diagram)

    @jwt_required()
    @namespace.doc(security="Bearer")
    def delete(self, diagram_item_id: str):
        dependency_injector.get(DiagramService).delete_diagram(utils.str_to_uuid(diagram_item_id))
