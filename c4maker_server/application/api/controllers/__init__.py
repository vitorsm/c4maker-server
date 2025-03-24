from flask_restx import Api
from injector import Injector

from c4maker_server import configs
from c4maker_server.application.api import app
from c4maker_server.application.api.security import authentication_utils
from c4maker_server.application.config.dependencies_injector import DependenciesInjector

from c4maker_server.application.api.models import models

dependency_injector = Injector([DependenciesInjector(app)])

api = Api(app, version=configs.VERSION, title="C4 maker API", description="C4 maker API")

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
namespace = api.namespace("", description="C4 maker API", authorizations=authorizations)

reduced_entity_model = api.model("ReducedEntity", models.get_reduced_entity_model())
reduced_user_model = api.model("ReducedUser", models.get_reduced_user_model())
reduced_workspace_model = api.model("ReducedWorkspace", models.get_reduced_workspace_model(reduced_user_model))
workspace_model = api.model("Workspace", models.get_workspace_model(reduced_user_model, reduced_workspace_model))
workspace_item_model = api.model("WorkspaceItem", models.get_workspace_item(reduced_user_model,
                                                                            reduced_workspace_model))

diagram_model = api.model("Diagram", models.get_diagram_model(reduced_user_model, reduced_workspace_model))
user_access_model = api.model("UserAccess", models.get_user_access_model(reduced_workspace_model))
user_model = api.model("User", models.get_user_model(user_access_model))
diagram_relationship_model = api.model("DiagramItemRelationship", models.get_relationship_model(reduced_entity_model))
diagram_item_model = api.model("DiagramItem", models.get_diagram_item(workspace_item_model, diagram_model,
                                                                      diagram_relationship_model, reduced_entity_model))

jwt = authentication_utils.fill_jwt_auth_function(app, dependency_injector)

from c4maker_server.application.api.controllers import error_handler
