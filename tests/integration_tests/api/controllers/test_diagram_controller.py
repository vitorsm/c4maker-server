from typing import Any

from tests.integration_tests.api.controllers.generic_controller_test import GenericControllerTest
from tests.integration_tests.base_integ_test import BaseIntegTest


class TestDiagramController(BaseIntegTest, GenericControllerTest):
    def _get_endpoint(self) -> str:
        return "/diagram"

    def _get_endpoint_by_id(self, entity_id: str):
        return f"{self._get_endpoint()}/{entity_id}"

    def _get_invalid_insert_payload(self) -> dict:
        return {
                "name": "",
                "description": "Test"
            }

    def _get_insert_payload(self) -> dict:
        return {
                "name": "Test name",
                "description": "Test description"
            }

    def get_client(self) -> Any:
        return self.client

    def get_default_id(self) -> str:
        return self.default_id

    def get_not_persisted_id(self) -> str:
        return self.not_persisted_id

    def setUp(self):
        self.create_app()
        super().setUp()
