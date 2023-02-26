import json

from flask.testing import FlaskClient

from c4maker_server.utils import date_utils
from tests.integration_tests.api.controllers.generic_controller_test import GenericControllerTest
from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues


class TestWorkspaceController(BaseIntegTest, GenericControllerTest):
    def _has_find_all(self) -> bool:
        return True

    def _get_endpoint(self) -> str:
        return "/workspace"

    def _get_endpoint_by_id(self, entity_id: str):
        return f"{self._get_endpoint()}/{entity_id}"

    def _get_invalid_insert_payload(self) -> dict:
        payload = self._get_insert_payload()
        payload["name"] = None
        return payload

    def _get_insert_payload(self) -> dict:
        return {
            "name": "new workspace",
            "description": "this is a new workspace"
        }

    def get_client(self) -> FlaskClient:
        return self.client

    def get_default_id(self) -> str:
        return str(DefaultValues.DEFAULT_ID)

    def get_not_persisted_id(self) -> str:
        return str(DefaultValues.NOT_PERSISTED_ID)

    def test_find_workspace_diagrams(self):
        # given
        valid_header = self.get_authentication_header()
        workspace_id = str(DefaultValues.DEFAULT_ID)
        address = self._get_endpoint_by_id(workspace_id) + "/diagrams"
        diagram = DefaultValues.get_default_diagram()

        # when
        response = self.get_client().get(address, headers=valid_header)

        # then
        response_dto = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)

        self.assertEqual(1, len(response_dto))
        self.assertEqual(str(diagram.id), response_dto[0]["id"])
        self.assertEqual(diagram.name, response_dto[0]["name"])
        self.assertEqual(date_utils.datetime_to_str(diagram.modified_at), response_dto[0]["modified_at"])
        self.assertEqual(date_utils.datetime_to_str(diagram.created_at), response_dto[0]["created_at"])
        self.assertEqual(str(diagram.created_by.id), response_dto[0]["created_by"]["id"])
        self.assertEqual(str(diagram.modified_by.id), response_dto[0]["modified_by"]["id"])
        self.assertEqual(str(diagram.workspace.id), response_dto[0]["workspace"]["id"])

    def test_find_workspace_diagram_invalid_workspace(self):
        # given
        valid_header = self.get_authentication_header()
        workspace_id = str(DefaultValues.NOT_PERSISTED_ID)
        address = self._get_endpoint_by_id(workspace_id) + "/diagrams"

        # when
        response = self.get_client().get(address, headers=valid_header)

        # then
        self.assertEqual(404, response.status_code)

    def test_find_workspace_diagram_invalid_user(self):
        # given
        valid_header = self.get_authentication_header_without_permission()
        workspace_id = str(DefaultValues.DEFAULT_ID)
        address = self._get_endpoint_by_id(workspace_id) + "/diagrams"

        # when
        response = self.get_client().get(address, headers=valid_header)

        # then
        self.assertEqual(403, response.status_code)

    def test_find_workspace_items(self):
        # given
        valid_header = self.get_authentication_header()
        workspace_id = str(DefaultValues.DEFAULT_ID)
        address = self._get_endpoint_by_id(workspace_id) + "/workspace-items"
        first_item = DefaultValues.get_default_workspace_item()
        second_item = DefaultValues.get_secondary_workspace_item()
        third_item = DefaultValues.get_other_workspace_item()

        # when
        response = self.get_client().get(address, headers=valid_header)

        # then
        response_dto = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)

        self.assertEqual(3, len(response_dto))

        self.assertEqual(str(first_item.id), response_dto[0]["id"])
        self.assertEqual(str(second_item.id), response_dto[1]["id"])
        self.assertEqual(str(third_item.id), response_dto[2]["id"])

        self.assertEqual(first_item.name, response_dto[0]["name"])
        self.assertEqual(second_item.name, response_dto[1]["name"])
        self.assertEqual(third_item.name, response_dto[2]["name"])

    def test_find_workspace_items_invalid_workspace(self):
        # given
        valid_header = self.get_authentication_header()
        workspace_id = str(DefaultValues.NOT_PERSISTED_ID)
        address = self._get_endpoint_by_id(workspace_id) + "/workspace-items"

        # when
        response = self.get_client().get(address, headers=valid_header)

        # then
        self.assertEqual(404, response.status_code)

    def test_find_workspace_items_invalid_user(self):
        # given
        valid_header = self.get_authentication_header_without_permission()
        workspace_id = str(DefaultValues.DEFAULT_ID)
        address = self._get_endpoint_by_id(workspace_id) + "/workspace-items"

        # when
        response = self.get_client().get(address, headers=valid_header)

        # then
        self.assertEqual(403, response.status_code)
