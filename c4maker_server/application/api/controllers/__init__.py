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

reduced_user_model = api.model("ReducedUser", models.get_reduced_user_model())
diagram_model = api.model("Diagram", models.get_diagram_model(reduced_user_model))
user_access_model = api.model("UserAccess", models.get_user_access_model(diagram_model))
user_model = api.model("User", models.get_user_model(user_access_model))
diagram_item_model = api.model("DiagramItem", models.get_diagram_item(reduced_user_model, diagram_model))

jwt = authentication_utils.fill_jwt_auth_function(app, dependency_injector)

from c4maker_server.application.api.controllers import error_handler
