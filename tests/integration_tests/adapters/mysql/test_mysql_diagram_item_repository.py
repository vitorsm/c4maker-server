from typing import Any
from uuid import UUID

from c4maker_server.adapters.mysql.mysql_diagram_item_repository import MySQLDiagramItemRepository
from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item import DiagramItemType, DiagramItem
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship
from c4maker_server.utils import date_utils
from tests.integration_tests.adapters.mysql.generic_mysql_test import GenericMySQLTest


class TestMySQLDiagramItemRepository(GenericMySQLTest):
    repository: MySQLDiagramItemRepository = None

    def get_repository(self) -> Any:
        if not self.repository:
            self.repository = MySQLDiagramItemRepository(self.mysql_client)

        return self.repository

    def get_default_entity(self) -> Any:
        diagram = Diagram(id=self.DEFAULT_ID, name=None, description=None)
        diagram_item2 = DiagramItem(id=UUID("00000000-0000-0000-0000-000000000002"), name=None, details=None,
                                    item_description=None, item_type=None, diagram=diagram)
        relationship1 = DiagramItemRelationship(diagram_item=diagram_item2, description="uses", details="details")

        created_at = date_utils.str_iso_to_date("2022-01-01T07:44:42.000")

        return DiagramItem(id=self.DEFAULT_ID, name="Item 1", item_description="Desc 1", details="Details 1",
                           item_type=DiagramItemType.PERSON, diagram=diagram, relationships=[relationship1],
                           parent=None, created_by=self.DEFAULT_USER, modified_by=self.DEFAULT_USER,
                           created_at=created_at, modified_at=created_at)

    def get_updated_default_entity(self) -> Any:
        default_entity = self.get_default_entity()

        default_entity.name = "modified name"
        default_entity.item_description = "modified description"
        default_entity.details = "modified details"
        default_entity.item_type = DiagramItemType.COMPONENT

        return default_entity

    def get_entity_name(self) -> str:
        return "DiagramItem"
