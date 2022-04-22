import unittest
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item import DiagramItem, DiagramItemType
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.diagram_item_service import DiagramItemService


class TestDiagramItemService(unittest.TestCase):

    def setUp(self):
        self.repository = Mock()
        self.diagram_service = Mock()
        self.service = DiagramItemService(self.repository, self.diagram_service)

        self.user1 = User(id=uuid4(), name="", login="", password="", shared_diagrams=[])
        self.diagram1 = Diagram(id=uuid4(), name="Diagram 1", description=None, created_by=self.user1,
                                created_at=datetime.now(), modified_by=self.user1, modified_at=datetime.now())
        self.diagram2 = Diagram(id=uuid4(), name="Diagram 2", description=None, created_by=self.user1,
                                created_at=datetime.now(), modified_by=self.user1, modified_at=datetime.now())
        self.diagram_item1 = DiagramItem(id=uuid4(), name="Item 1", item_description="Description", details="Details",
                                         item_type=DiagramItemType.COMPONENT, diagram=self.diagram1,
                                         created_at=datetime.now(), modified_at=datetime.now(), created_by=self.user1,
                                         modified_by=self.user1)

    def test_create_item_diagram_success(self):
        diagram_item = DiagramItem(id=None, name="name", item_description="description", details="details",
                                   item_type=DiagramItemType.COMPONENT, diagram=Diagram(id=self.diagram1.id, name="",
                                                                                        description=None))

        self.repository.create.return_value = None
        self.diagram_service.find_diagram_by_id.return_value = self.diagram1
        self.diagram_service.check_permission_to_persist.return_value = True

        self.service.create_diagram_item(diagram_item, self.user1)

        self.assertEqual(1, self.repository.create.call_count)

    def test_create_item_diagram_missing_fields(self):
        diagram_item = DiagramItem(id=None, name="", item_description="", details="",
                                   item_type=DiagramItemType.COMPONENT, diagram=Diagram(id=self.diagram1.id, name="",
                                                                                        description=None))

        self.repository.create.return_value = None
        self.diagram_service.find_diagram_by_id.return_value = None
        self.diagram_service.check_permission_to_persist.return_value = True

        with self.assertRaises(InvalidEntityException) as exception_context:
            self.service.create_diagram_item(diagram_item, self.user1)

        self.assertEqual(0, self.repository.create.call_count)
        self.assertIn("diagram, name, details, item_description", str(exception_context.exception))

    def test_update_diagram_item_success(self):
        diagram_item = DiagramItem(id=self.diagram_item1.id, name="name", item_description="description",
                                   details="details", item_type=DiagramItemType.COMPONENT,
                                   diagram=Diagram(id=self.diagram1.id, name="", description=None))

        self.repository.update.return_value = None
        self.repository.find_by_id.return_value = self.diagram_item1
        self.diagram_service.find_diagram_by_id.return_value = self.diagram1
        self.diagram_service.check_permission_to_persist.return_value = True

        self.service.update_diagram_item(diagram_item, self.user1)

        self.assertEqual(1, self.repository.update.call_count)
        self.assertIsNotNone(diagram_item.created_by)
        self.assertIsNotNone(diagram_item.created_at)
        self.assertIsNotNone(diagram_item.modified_at)
        self.assertIsNotNone(diagram_item.modified_by)

    def test_update_diagram_item_missing_fields(self):
        diagram_item = DiagramItem(id=self.diagram_item1.id, name="", item_description="", details="",
                                   item_type=DiagramItemType.COMPONENT, diagram=Diagram(id=self.diagram1.id, name="",
                                                                                        description=None))

        self.repository.update.return_value = None
        self.diagram_service.find_diagram_by_id.return_value = None
        self.diagram_service.check_permission_to_persist.return_value = True

        with self.assertRaises(InvalidEntityException) as exception_context:
            self.service.update_diagram_item(diagram_item, self.user1)

        self.assertEqual(0, self.repository.update.call_count)
        self.assertIn("diagram, name, details, item_description", str(exception_context.exception))

    def test_update_diagram_item_different_diagram(self):
        diagram_item = DiagramItem(id=self.diagram_item1.id, name="name", item_description="description",
                                   details="details", item_type=DiagramItemType.COMPONENT,
                                   diagram=Diagram(id=self.diagram2.id, name="", description=None))

        self.repository.update.return_value = None
        self.diagram_service.find_diagram_by_id.return_value = self.diagram2
        self.diagram_service.check_permission_to_persist.return_value = True

        with self.assertRaises(InvalidEntityException) as exception_context:
            self.service.update_diagram_item(diagram_item, self.user1)

        self.assertEqual(0, self.repository.update.call_count)
        self.assertIn("diagram", str(exception_context.exception))

    def test_delete_diagram_item_success(self):
        self.repository.find_by_id.return_value = self.diagram_item1
        self.diagram_service.find_diagram_by_id.return_value = self.diagram1
        self.diagram_service.check_permission_to_persist.return_value = True

        self.repository.delete.return_value = None

        self.service.delete_diagram_item(self.diagram_item1.id, self.user1)

        self.assertEqual(1, self.repository.delete.call_count)

    def test_delete_diagram_without_permission(self):
        self.repository.find_by_id.return_value = self.diagram_item1
        self.diagram_service.find_diagram_by_id.return_value = self.diagram1

        self.diagram_service.check_permission_to_persist.side_effect = \
            PermissionException('Test', self.diagram1.id, self.user1)

        self.repository.delete.return_value = None

        with self.assertRaises(PermissionException):
            self.service.delete_diagram_item(self.diagram_item1.id, self.user1)

        self.assertEqual(0, self.repository.delete.call_count)

    def test_delete_diagram_item_without_diagram(self):
        self.repository.find_by_id.return_value = self.diagram_item1
        self.diagram_service.find_diagram_by_id.side_effect = EntityNotFoundException("Diagram", self.diagram1.id)
        self.diagram_service.check_permission_to_persist.return_value = True

        self.repository.delete.return_value = None

        with self.assertRaises(EntityNotFoundException):
            self.service.delete_diagram_item(self.diagram_item1.id, self.user1)

        self.assertEqual(0, self.repository.delete.call_count)
