from flask import request
from flask_jwt import jwt_required
from flask_restx import Resource

from c4maker_server.application.api.controllers import namespace, diagram_item_model, dependency_injector
from c4maker_server.application.api.mapper.diagram_item_mapper import DiagramItemMapper
from c4maker_server.services.diagram_item_service import DiagramItemService
from c4maker_server.utils import utils


@namespace.route("/diagram-item")
class DiagramItemController(Resource):

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.expect(diagram_item_model, validate=True)
    @namespace.marshal_with(diagram_item_model)
    def post(self):
        payload = request.get_json()
        diagram_item = DiagramItemMapper.to_entity(payload)
        dependency_injector.get(DiagramItemService).create_diagram_item(diagram_item)

        return DiagramItemMapper.to_dto(diagram_item), 201


@namespace.route("/diagram-item/<string:diagram_item_id>")
class DiagramItemEntityController(Resource):

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.expect(diagram_item_model, validate=True)
    @namespace.marshal_with(diagram_item_model)
    def put(self, diagram_item_id: str):
        payload = request.get_json()
        diagram_item = DiagramItemMapper.to_entity(payload)
        diagram_item.id = utils.str_to_uuid(diagram_item_id)
        dependency_injector.get(DiagramItemService).update_diagram_item(diagram_item)

        return DiagramItemMapper.to_dto(diagram_item)

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(diagram_item_model)
    def get(self, diagram_item_id: str):
        diagram = dependency_injector.get(DiagramItemService).find_diagram_item_by_id(utils.str_to_uuid(diagram_item_id))

        return DiagramItemMapper.to_dto(diagram)

    @jwt_required()
    @namespace.doc(security="Bearer")
    def delete(self, diagram_item_id: str):
        dependency_injector.get(DiagramItemService).delete_diagram_item(utils.str_to_uuid(diagram_item_id))
        return None, 204
