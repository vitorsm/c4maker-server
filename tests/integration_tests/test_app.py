from flask import Flask

SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
TESTING = True
ENCRYPT_SECRET_KEY = "tests"

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = ENCRYPT_SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_AUTH_HEADER_PREFIX'] = "Bearer"
