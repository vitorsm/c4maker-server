from typing import Any
from unittest import TestCase

from c4maker_server.adapters.mysql.mysql_workspace_repository import MySQLWorkspaceRepository
from tests.integration_tests.adapters.mysql.generic_mysql_test import GenericMySQLTest
from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues


class TestMySQLWorkspaceRepository(GenericMySQLTest, BaseIntegTest):
    repository: MySQLWorkspaceRepository = None

    def get_test_case(self) -> TestCase:
        return self

    def get_repository(self) -> Any:
        if not self.repository:
            self.repository = MySQLWorkspaceRepository(self.mysql_client)

        return self.repository

    def get_default_entity(self) -> Any:
        return DefaultValues.get_default_workspace()

    def get_updated_default_entity(self) -> Any:
        default_entity = self.get_default_entity()
        default_entity.name = "modified name"
        default_entity.description = "modified description"

        return default_entity

    def get_entity_name(self) -> str:
        return "Workspace"

    def test_find_workspaces_by_user(self):
        # given
        user = DefaultValues.get_default_user()

        # when
        workspaces = self.get_repository().find_all_by_user(user)

        # then
        self.assertEqual(1, len(workspaces))
        self.compare_obj_properties(self.get_default_entity(), workspaces[0])
