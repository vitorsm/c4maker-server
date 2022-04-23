import os
from unittest import TestCase
from uuid import UUID

from flask import Flask
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from c4maker_server.adapters.models import BaseModel
from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.domain.entities.user import User


class BaseIntegTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    ENCRYPT_SECRET_KEY = "tests"
    DEFAULT_ID = UUID("00000000-0000-0000-0000-000000000000")
    DEFAULT_USER = User(id=DEFAULT_ID, name="User 1", login="user", password="12345", shared_diagrams=[])

    app: Flask
    mysql_client: MySQLClient
    jwt: JWT
    token: str

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = self.ENCRYPT_SECRET_KEY
        self.app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"

        db = SQLAlchemy(self.app, session_options={"autoflush": False})
        self.mysql_client = MySQLClient(db)

        return self.app

    def setUp(self):
        BaseModel.metadata.create_all(self.mysql_client.db.get_engine())
        self.initial_load()
        self.mysql_client.db.session.commit()

    def initial_load(self):
        file_path = BaseIntegTest.get_project_dir() + "resources/initial_load.sql"
        file = open(file_path)
        for query in file.read().split(";"):
            if query.strip():
                self.mysql_client.db.session.execute(query.strip())
        file.close()

    def tearDown(self):
        self.mysql_client.db.session.remove()
        self.mysql_client.db.drop_all()

    @staticmethod
    def get_project_dir():
        path = os.getcwd()
        return path.split("c4maker-server")[0] + "c4maker-server/"
