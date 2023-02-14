from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from c4maker_server import configs
from c4maker_server.application.api.security import authentication_utils
from c4maker_server.application.api.models.models import get_reduced_user_model, get_diagram_model, \
    get_user_access_model, get_user_model, get_diagram_item

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = configs.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = configs.ENCRYPT_SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=configs.HOURS_TO_EXPIRATION_TOKEN)
app.config['JWT_AUTH_HEADER_PREFIX'] = "Bearer"
