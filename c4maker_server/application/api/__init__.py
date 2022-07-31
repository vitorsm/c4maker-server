from datetime import timedelta

from flask import Flask
from flask_restx import Api
from injector import Injector

from c4maker_server import configs
from c4maker_server.application.api.security import authentication_utils
from c4maker_server.application.config.dependencies_injector import DependenciesInjector
from c4maker_server.application.api.models.models import get_reduced_user_model, get_diagram_model, \
    get_user_access_model, get_user_model, get_diagram_item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = configs.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = configs.ENCRYPT_SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=configs.HOURS_TO_EXPIRATION_TOKEN)
app.config['JWT_AUTH_HEADER_PREFIX'] = "Bearer"

dependency_injector = Injector([DependenciesInjector(app)])

api = Api(app, version=configs.VERSION, title="C4 maker API", description="C4 maker API")

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
namespace = api.namespace("", description="C4 maker API", authorizations=authorizations)

reduced_user_model = api.model("ReducedUser", get_reduced_user_model())
diagram_model = api.model("Diagram", get_diagram_model(reduced_user_model))
user_access_model = api.model("UserAccess", get_user_access_model(diagram_model))
user_model = api.model("User", get_user_model(user_access_model))
diagram_item_model = api.model("DiagramItem", get_diagram_item(reduced_user_model, diagram_model))

jwt = authentication_utils.fill_jwt_auth_function(app, dependency_injector)
