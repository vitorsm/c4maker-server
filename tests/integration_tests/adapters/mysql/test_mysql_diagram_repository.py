from typing import Any
from unittest import TestCase

from c4maker_server.adapters.mysql.mysql_diagram_repository import MySQLDiagramRepository
from c4maker_server.domain.entities.diagram import Diagram, DiagramType
from c4maker_server.utils import date_utils
from tests.integration_tests.adapters.mysql.generic_mysql_test import GenericMySQLTest
from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues
from tests.utils.obj_mother import ObjMother


class TestMySQLDiagramRepository(GenericMySQLTest, BaseIntegTest):
    repository: MySQLDiagramRepository = None

    def setUp(self):
        self.create_app()
        super().setUp()

    def get_repository(self) -> Any:
        if not self.repository:
            self.repository = MySQLDiagramRepository(self.mysql_client)

        return self.repository

    def get_test_case(self) -> TestCase:
        return self

    def get_default_entity(self) -> Any:
        return DefaultValues.get_default_diagram()

    def get_updated_default_entity(self) -> Any:
        default_entity = self.get_default_entity()
        default_entity.name = "modified name"
        default_entity.description = "modified description"

        return default_entity

    def get_entity_name(self) -> str:
        return "Diagram"
