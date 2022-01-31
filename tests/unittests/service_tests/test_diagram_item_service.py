import unittest
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.user import User
from c4maker_server.services.diagram_item_service import DiagramItemService


class TestDiagramItemService(unittest.TestCase):

    def setUp(self):
        self.repository = Mock()
        self.diagram_service = Mock()
        self.service = DiagramItemService(self.repository, self.diagram_service)

        self.user1 = User(id=uuid4(), name="", login="", password="", shared_diagrams=[])
        self.diagram1 = Diagram(id=uuid4(), name="Diagram 1", description=None, created_by=self.user1,
                                created_at=datetime.now(), modified_by=self.user1, modified_at=datetime.now())

        self.

    def test_create_item_diagram_success(self):

