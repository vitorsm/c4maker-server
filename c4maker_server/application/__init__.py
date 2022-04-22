from datetime import timedelta

from flask import Flask
from injector import Injector

from c4maker_server import configs
from c4maker_server.application.config.dependencies_injector import DependenciesInjector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = configs.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = configs.ENCRYPT_SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = "/v1/auth/authenticate"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=configs.HOURS_TO_EXPIRATION_TOKEN)

dependency_injector = Injector([DependenciesInjector(app)])

