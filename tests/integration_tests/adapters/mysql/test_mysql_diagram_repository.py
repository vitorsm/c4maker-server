from c4maker_server.adapters.mysql.mysql_diagram_repository import MySQLDiagramRepository
from tests.integration_tests.base_integ_test import BaseIntegTest


class TestMySQLDiagramRepository(BaseIntegTest):

    def setUp(self):
        super().setUp()
        self.repository = MySQLDiagramRepository(self.mysql_client)

    def test_find_diagram(self):
        diagram = self.repository.find_by_id(self.DEFAULT_ID)

        self.assertEqual("Diagram 1", diagram.name)
        self.assertEqual("Desc 1", diagram.description)
        self.assertEqual(self.DEFAULT_ID, diagram.created_by.id)
        self.assertEqual(self.DEFAULT_ID, diagram.modified_by.id)
