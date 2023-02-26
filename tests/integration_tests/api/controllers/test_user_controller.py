import json

from parameterized import parameterized

from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues


class TestUserController(BaseIntegTest):

    def test_create_user(self):
        # given
        user = {
            "login": "new_login",
            "name": "New user",
            "password": "12345"
        }
        address = "/user"

        # when
        response = self.client.post(address, json=user)

        # then
        self.assertEqual(201, response.status_code)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(user["login"], response_dto["login"])
        self.assertEqual(user["name"], response_dto["name"])

    @parameterized.expand([
        ({
            "login": "",
            "name": "New user",
            "password": "12345"
        },),
        ({
            "login": "new_login",
            "name": "",
            "password": "12345"
        },),
        ({
            "login": "new_login",
            "name": "New user",
            "password": ""
        },)
    ])
    def test_create_user_without_fields(self, user: dict):
        # given
        address = "/user"

        # when
        response = self.client.post(address, json=user)

        # then
        self.assertEqual(400, response.status_code)

    def test_get_current_user(self):
        # given
        valid_header = self.get_authentication_header()
        address = "/user/me"
        user = DefaultValues.get_default_user()

        # when
        response = self.client.get(address, headers=valid_header)

        # then
        self.assertEqual(200, response.status_code)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(str(user.id), response_dto["id"])
        self.assertEqual(user.name, response_dto["name"])
        self.assertEqual(user.login, response_dto["login"])
