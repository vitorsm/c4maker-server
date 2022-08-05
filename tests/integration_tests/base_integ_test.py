import os
from flask_testing import TestCase

from tests.integration_tests.test_app import app
import c4maker_server.application.api as api
api.app = app

from c4maker_server.application import controllers_imports
import uuid
from uuid import UUID

from flask import Flask

from c4maker_server.adapters.models import BaseModel
from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.application.api.controllers import dependency_injector, jwt
from c4maker_server.domain.entities.user import User


class BaseIntegTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    ENCRYPT_SECRET_KEY = "tests"
    DEFAULT_ID = UUID("00000000-0000-0000-0000-000000000000")
    DEFAULT_USER = User(id=DEFAULT_ID, name="User 1", login="user", password="12345", shared_diagrams=[])

    app: Flask
    mysql_client: MySQLClient
    token: str

    def create_app(self):
        self.app = app

        self.mysql_client = dependency_injector.get(MySQLClient)

        self.default_id = str(BaseIntegTest.DEFAULT_ID)
        self.secondary_default_id = "00000000-0000-0000-0000-000000000001"
        self.not_persisted_id = "00000000-0000-0000-0000-000000000099"

        self.default_user = self.__get_default_user()
        self.secondary_user = self.__get_secondary_user()

        return self.app

    def setUp(self):
        BaseModel.metadata.drop_all(self.mysql_client.db.get_engine())
        BaseModel.metadata.create_all(self.mysql_client.db.get_engine())
        self.initial_load()
        self.mysql_client.db.session.commit()

        default_user = self.default_user
        default_user.id = str(default_user.id)
        secondary_user = self.secondary_user
        secondary_user.id = str(secondary_user.id)

        self.token = "Bearer " + jwt.jwt_encode_callback(default_user).decode()
        self.secondary_token = "Bearer " + jwt.jwt_encode_callback(secondary_user).decode()

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

    def __get_default_user(self) -> User:
        return User(id=uuid.UUID(self.default_id), name="User 1", login="user", password="12345",
                    shared_diagrams=list())

    def __get_secondary_user(self) -> User:
        return User(id=uuid.UUID(self.secondary_default_id), name="User 2", login="user2", password="12345",
                    shared_diagrams=list())

    @staticmethod
    def get_project_dir():
        path = os.getcwd()
        return path.split("c4maker-server")[0] + "c4maker-server/"

    def get_authentication_header(self) -> dict:
        return {
            "Authorization": self.token
        }

    def get_authentication_header_without_permission(self) -> dict:
        return {
            "Authorization": self.secondary_token
        }
