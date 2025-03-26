from typing import Any

from tests.integration_tests.api.controllers.generic_controller_test import GenericControllerTest
from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues


class TestDiagramItemController(BaseIntegTest, GenericControllerTest):
    def _has_find_all(self) -> bool:
        return False

    def _get_endpoint(self) -> str:
        return "/diagram-item"

    def _get_endpoint_by_id(self, entity_id: str):
        return f"{self._get_endpoint()}/{entity_id}"

    def _get_invalid_insert_payload(self) -> dict:
        item = self._get_insert_payload()
        item["workspace_item"] = None
        return item

    def _get_insert_payload(self) -> dict:
        return {
            "workspace_item": {
                "id": self.get_default_id(),
                "name": "item 1",
                "key": "item1",
                "workspace_item_type": "DATABASE",
                "workspace": {
                    "id": self.get_default_id()
                }
            },
            "diagram": {"id": "00000000-0000-0000-0000-000000000000"},
            "parent": {"id": "00000000-0000-0000-0000-000000000001"},
            "diagram_item_type": "C4",
            "data": {
                "position": {
                    "x": 1,
                    "y": 1,
                    "width": 10,
                    "height": 10
                },
                "color": "white"
            },
            "relationships": [
                {
                    "diagram_item": {
                        "id": "00000000-0000-0000-0000-000000000001"
                    },
                    "description": "Description",
                    "details": "Details",
                    "diagram_type": "C4",
                    "data": {
                        "from_position": {
                            "x": 1,
                            "y": 1,
                            "width": 10,
                            "height": 10
                        },
                        "to_position": {
                            "x": 1,
                            "y": 1,
                            "width": 10,
                            "height": 10
                        }
                    }
                }
            ]
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
