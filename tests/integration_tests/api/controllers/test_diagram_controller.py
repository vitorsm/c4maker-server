from typing import Any

from tests.integration_tests.api.controllers.generic_controller_test import GenericControllerTest
from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues


class TestDiagramController(BaseIntegTest, GenericControllerTest):
    def _has_find_all(self) -> bool:
        return True

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
        return str(DefaultValues.DEFAULT_ID)

    def get_not_persisted_id(self) -> str:
        return str(DefaultValues.NOT_PERSISTED_ID)

    def setUp(self):
        self.create_app()
        super().setUp()
