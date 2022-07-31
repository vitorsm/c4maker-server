import unittest
from copy import deepcopy
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.user_access import UserAccess, UserPermission
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.diagram_service import DiagramService


class TestDiagramService(unittest.TestCase):

    def setUp(self):
        self.repository = Mock()
        self.authentication_repository = Mock()
        self.service = DiagramService(self.repository, self.authentication_repository)

        self.user1 = User(id=uuid4(), name="", login="", password="", shared_diagrams=[])
        self.user2 = User(id=uuid4(), name="", login="", password="", shared_diagrams=[])

        self.authentication_repository.get_current_user.return_value = self.user1

        self.diagram1 = Diagram(id=uuid4(), name="Diagram 1", description=None, created_by=self.user2,
                                created_at=datetime.now(), modified_by=self.user2, modified_at=datetime.now())
        self.diagram2 = Diagram(id=uuid4(), name="Diagram 1", description=None, created_by=self.user2)

    def test_create_diagram_success(self):
        diagram = Diagram(id=None, name="Diagram 1", description=None)
        self.repository.create.return_value = None

        self.service.create_diagram(diagram)

        self.assertEqual(1, self.repository.create.call_count)
        self.assertIsNotNone(diagram.created_by)
        self.assertIsNotNone(diagram.created_at)
        self.assertIsNotNone(diagram.modified_by)
        self.assertIsNotNone(diagram.modified_at)

    def test_create_diagram_without_name(self):
        diagram = Diagram(id=None, name="", description=None)
        self.repository.create.return_value = None

        with self.assertRaises(InvalidEntityException):
            self.service.create_diagram(diagram)

        self.assertEqual(0, self.repository.create.call_count)

    def test_update_diagram_owner_success(self):
        self.repository.update.return_value = None
        self.repository.find_by_id.return_value = self.diagram1

        new_name = "new name"
        new_description = "new description"
        diagram = Diagram(id=self.diagram1.id, name=new_name, description=new_description)
        self.authentication_repository.get_current_user.return_value = self.user2

        self.service.update_diagram(diagram)

        self.assertEqual(1, self.repository.update.call_count)
        self.assertEqual(new_name, diagram.name)
        self.assertEqual(new_description, diagram.description)
        self.assertIsNotNone(diagram.created_by)
        self.assertIsNotNone(diagram.created_at)
        self.assertIsNotNone(diagram.modified_by)
        self.assertIsNotNone(diagram.modified_at)

    def test_update_diagram_shared_success(self):
        self.repository.update.return_value = None
        self.repository.find_by_id.return_value = self.diagram1

        # user = deepcopy(self.user1)
        self.user1.shared_diagrams = [UserAccess(diagram=self.diagram1, permission=UserPermission.EDIT)]

        self.service.update_diagram(self.diagram1)

        self.assertEqual(1, self.repository.update.call_count)

    def test_update_diagram_shared_view_failed(self):
        self.repository.update.return_value = None
        self.repository.find_by_id.return_value = self.diagram1

        self.user1.shared_diagrams = [UserAccess(diagram=self.diagram1, permission=UserPermission.VIEW)]

        with self.assertRaises(PermissionException):
            self.service.update_diagram(self.diagram1)

        self.assertEqual(0, self.repository.update.call_count)

    def test_update_diagram_shared_other_edit_failed(self):
        self.repository.update.return_value = None
        self.repository.find_by_id.return_value = self.diagram2

        self.user1.shared_diagrams = [UserAccess(diagram=self.diagram1, permission=UserPermission.EDIT)]

        with self.assertRaises(PermissionException):
            self.service.update_diagram(self.diagram2)

        self.assertEqual(0, self.repository.update.call_count)

    def test_update_diagram_not_found_failed(self):
        self.repository.update.return_value = None
        self.repository.find_by_id.return_value = None

        self.user1.shared_diagrams = [UserAccess(diagram=self.diagram1, permission=UserPermission.EDIT)]

        with self.assertRaises(EntityNotFoundException):
            self.service.update_diagram(self.diagram2)

        self.assertEqual(0, self.repository.update.call_count)

    def test_update_diagram_without_name_failed(self):
        self.repository.update.return_value = None
        self.repository.find_by_id.return_value = self.diagram2

        diagram = deepcopy(self.diagram2)
        self.user1.shared_diagrams = [UserAccess(diagram=diagram, permission=UserPermission.EDIT)]

        diagram.name = ""

        with self.assertRaises(InvalidEntityException):
            self.service.update_diagram(diagram)

        self.assertEqual(0, self.repository.update.call_count)

    def test_delete_diagram_success(self):
        diagram_id = self.diagram1.id
        self.repository.delete.return_value = None
        self.repository.find_by_id.return_value = self.diagram1
        self.authentication_repository.get_current_user.return_value = self.user2

        self.service.delete_diagram(diagram_id)

        self.assertEqual(1, self.repository.delete.call_count)

    def test_delete_without_permission(self):
        diagram_id = self.diagram1.id

        self.user1.id = uuid4()
        self.user1.shared_diagrams = [UserAccess(diagram=self.diagram1, permission=UserPermission.EDIT)]
        self.repository.delete.return_value = None
        self.repository.find_by_id.return_value = self.diagram1

        with self.assertRaises(PermissionException):
            self.service.delete_diagram(diagram_id)

        self.assertEqual(0, self.repository.delete.call_count)

    def test_delete_not_found_permission(self):
        diagram_id = self.diagram1.id

        self.user1.id = uuid4()
        self.user1.shared_diagrams = [UserAccess(diagram=self.diagram1, permission=UserPermission.EDIT)]
        self.repository.delete.return_value = None
        self.repository.find_by_id.return_value = None

        with self.assertRaises(EntityNotFoundException):
            self.service.delete_diagram(diagram_id)

        self.assertEqual(0, self.repository.delete.call_count)
