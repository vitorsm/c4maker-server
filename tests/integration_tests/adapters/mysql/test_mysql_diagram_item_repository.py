from typing import Any
from unittest import TestCase
from uuid import UUID

from c4maker_server.adapters.mysql.mysql_diagram_item_repository import MySQLDiagramItemRepository
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.utils import date_utils
from tests.integration_tests.adapters.mysql.generic_mysql_test import GenericMySQLTest
from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues
from tests.utils.obj_mother import ObjMother


class TestMySQLDiagramItemRepository(GenericMySQLTest, BaseIntegTest):
    repository: MySQLDiagramItemRepository = None

    def setUp(self):
        self.create_app()
        super().setUp()

    def get_repository(self) -> Any:
        if not self.repository:
            self.repository = MySQLDiagramItemRepository(self.mysql_client)

        return self.repository

    def get_test_case(self) -> TestCase:
        return self

    def get_default_entity(self) -> Any:
        return DefaultValues.get_default_diagram_item()

    def get_updated_default_entity(self) -> Any:
        default_entity = self.get_default_entity()
        default_entity.workspace_item = DefaultValues.get_secondary_workspace_item()

        return default_entity

    def get_entity_name(self) -> str:
        return "DiagramItem"

    def test_find_all_by_diagram(self):
        # given
        diagram = DefaultValues.get_default_diagram()

        # when
        diagram_items = self.get_repository().find_all_by_diagram(diagram)

        # then
        self.assertEqual(3, len(diagram_items))
        self.compare_obj_properties(DefaultValues.get_default_diagram_item(), diagram_items[0])
