from typing import Any
from unittest import TestCase

from c4maker_server.adapters.mysql.mysql_workspace_item_repository import MySQLWorkspaceItemRepository
from tests.integration_tests.adapters.mysql.generic_mysql_test import GenericMySQLTest
from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues


class TestMySQLWorkspaceItemRepository(GenericMySQLTest, BaseIntegTest):
    repository: MySQLWorkspaceItemRepository = None

    def get_test_case(self) -> TestCase:
        return self

    def get_repository(self) -> Any:
        if not self.repository:
            self.repository = MySQLWorkspaceItemRepository(self.mysql_client)
        return self.repository

    def get_default_entity(self) -> Any:
        return DefaultValues.get_default_workspace_item()

    def get_updated_default_entity(self) -> Any:
        default_entity = self.get_default_entity()
        default_entity.name = "new name"
        default_entity.details = None
        default_entity.description = "new description"

        return default_entity

    def get_entity_name(self) -> str:
        return "WorkspaceItem"

    def test_find_all_by_workspace(self):
        # given
        workspace_id = DefaultValues.DEFAULT_ID

        # when
        workspace_items = self.get_repository().find_items_by_workspace(workspace_id)

        # then
        self.assertEqual(3, len(workspace_items))
        self.compare_obj_properties(DefaultValues.get_default_workspace_item(), workspace_items[0])
        self.compare_obj_properties(DefaultValues.get_secondary_workspace_item(), workspace_items[1])
        self.compare_obj_properties(DefaultValues.get_other_workspace_item(), workspace_items[2])
