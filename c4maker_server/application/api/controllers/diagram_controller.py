from flask import request
from flask_jwt import jwt_required
from flask_restx import Resource

from c4maker_server.application.api.controllers import namespace, diagram_model, dependency_injector, diagram_item_model
from c4maker_server.application.api.mapper.diagram_item_mapper import DiagramItemMapper
from c4maker_server.application.api.mapper.diagram_mapper import DiagramMapper
from c4maker_server.services.diagram_item_service import DiagramItemService
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


@namespace.route("/diagram/<string:diagram_id>")
class DiagramEntityController(Resource):

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.expect(diagram_model, validate=True)
    @namespace.marshal_with(diagram_model)
    def put(self, diagram_id: str):
        payload = request.get_json()
        diagram = DiagramMapper.to_entity(payload)
        diagram.id = utils.str_to_uuid(diagram_id)
        dependency_injector.get(DiagramService).update_diagram(diagram)

        return DiagramMapper.to_dto(diagram)

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(diagram_model)
    def get(self, diagram_id: str):
        diagram = dependency_injector.get(DiagramService).find_diagram_by_id(utils.str_to_uuid(diagram_id))

        return DiagramMapper.to_dto(diagram)

    @jwt_required()
    @namespace.doc(security="Bearer")
    def delete(self, diagram_id: str):
        dependency_injector.get(DiagramService).delete_diagram(utils.str_to_uuid(diagram_id))
        return None, 204


@namespace.route("/diagram/<string:diagram_id>/diagram-items")
class DiagramItemsByDiagramEntityController(Resource):
    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(diagram_item_model)
    def get(self, diagram_id: str):
        diagram_id = utils.str_to_uuid(diagram_id)
        diagram_items = dependency_injector.get(DiagramItemService).find_diagram_items_by_diagram(diagram_id)

        return [DiagramItemMapper.to_dto(diagram_item) for diagram_item in diagram_items]
