from flask import request
from flask_jwt import jwt_required
from flask_restx import Resource

from c4maker_server.application.api.controllers import namespace, workspace_model, dependency_injector, \
    workspace_item_model, diagram_model
from c4maker_server.application.api.mapper.diagram_mapper import DiagramMapper
from c4maker_server.application.api.mapper.workspace_item_mapper import WorkspaceItemMapper
from c4maker_server.application.api.mapper.workspace_mapper import WorkspaceMapper
from c4maker_server.services.diagram_service import DiagramService
from c4maker_server.services.workspace_item_service import WorkspaceItemService
from c4maker_server.services.workspace_service import WorkspaceService
from c4maker_server.utils import utils


@namespace.route("/workspace")
class WorkspaceController(Resource):

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.expect(workspace_model, validate=True)
    @namespace.marshal_with(workspace_model)
    def post(self):
        payload = request.get_json()
        workspace = WorkspaceMapper.to_entity(payload)
        dependency_injector.get(WorkspaceService).create_workspace(workspace)

        return WorkspaceMapper.to_dto(workspace), 201

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(workspace_model)
    def get(self):
        workspaces = dependency_injector.get(WorkspaceService).find_workspaces_by_user()
        return [WorkspaceMapper.to_dto(workspace) for workspace in workspaces]


@namespace.route("/workspace/<string:workspace_id>")
class WorkspaceById(Resource):

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(workspace_model)
    def get(self, workspace_id: str):
        workspace_id = utils.str_to_uuid(workspace_id)
        workspace = dependency_injector.get(WorkspaceService).find_workspace_by_id(workspace_id)
        return WorkspaceMapper.to_dto(workspace)

    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.expect(workspace_model)
    @namespace.marshal_with(workspace_model)
    def put(self, workspace_id: str):
        payload = request.get_json()
        workspace = WorkspaceMapper.to_entity(payload)
        workspace.id = utils.str_to_uuid(workspace_id)
        dependency_injector.get(WorkspaceService).update_workspace(workspace)

        return WorkspaceMapper.to_dto(workspace), 200
# 70-71,76-82,94-100,106,131,139
    @jwt_required()
    @namespace.doc(security="Bearer")
    def delete(self, workspace_id: str):
        dependency_injector.get(WorkspaceService).delete_workspace(utils.str_to_uuid(workspace_id))
        return None, 204


@namespace.route("/workspace/<string:workspace_id>/diagrams")
class DiagramsByWorkspace(Resource):
    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(diagram_model)
    def get(self, workspace_id: str):
        workspace_id = utils.str_to_uuid(workspace_id)
        diagrams = dependency_injector.get(DiagramService).find_diagrams_by_workspace(workspace_id)
        return [DiagramMapper.to_dto(diagram) for diagram in diagrams]


@namespace.route("/workspace/<string:workspace_id>/workspace-items")
class WorkspaceItemsByWorkspace(Resource):
    @jwt_required()
    @namespace.doc(security="Bearer")
    @namespace.marshal_with(workspace_item_model)
    def get(self, workspace_id: str):
        workspace_id = utils.str_to_uuid(workspace_id)
        workspace_items = dependency_injector.get(WorkspaceItemService).find_items_by_workspace(workspace_id)
        return [WorkspaceItemMapper.to_dto(workspace_item) for workspace_item in workspace_items]
