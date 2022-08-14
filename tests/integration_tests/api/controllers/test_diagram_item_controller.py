from typing import Any

from tests.integration_tests.api.controllers.generic_controller_test import GenericControllerTest
from tests.integration_tests.base_integ_test import BaseIntegTest


class TestDiagramItemController(BaseIntegTest, GenericControllerTest):
    def _has_find_all(self) -> bool:
        return False

    def _get_endpoint(self) -> str:
        return "/diagram-item"

    def _get_endpoint_by_id(self, entity_id: str):
        return f"{self._get_endpoint()}/{entity_id}"

    def _get_invalid_insert_payload(self) -> dict:
        item = self._get_insert_payload()
        item["item_type"] = None
        return item

    def _get_insert_payload(self) -> dict:
        return {
            "name": "Test name",
            "item_description": "Test description",
            "details": "Test details",
            "item_type": "SOFTWARE_SYSTEM",
            "diagram": {"id": "00000000-0000-0000-0000-000000000000"},
            "parent": {"id": "00000000-0000-0000-0000-000000000001"}
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
