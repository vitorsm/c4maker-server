import unittest
from copy import deepcopy
from datetime import datetime
from typing import List
from unittest.mock import Mock
from uuid import uuid4

from parameterized import parameterized

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.user_access import UserAccess, UserPermission
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.diagram_item_service import DiagramItemService
from tests.utils.obj_mother import ObjMother


current_user = ObjMother.generate_random_user()

workspace1 = ObjMother.generate_random_workspace(user=current_user)
workspace_item1 = ObjMother.generate_random_workspace_item(workspace=workspace1)
workspace_item11 = ObjMother.generate_random_workspace_item(workspace=workspace1)
diagram1 = ObjMother.generate_random_diagram(workspace=workspace1)
diagram11 = ObjMother.generate_random_diagram(workspace=workspace1)
persisted_item1 = ObjMother.generate_random_diagram_item(workspace_item=workspace_item1, diagram=diagram1)

workspace2 = ObjMother.generate_random_workspace()
workspace_item2 = ObjMother.generate_random_workspace_item(workspace=workspace2)
diagram2 = ObjMother.generate_random_diagram(workspace=workspace2)
persisted_item2 = ObjMother.generate_random_diagram_item(workspace_item=workspace_item2, diagram=diagram2)

workspace3 = ObjMother.generate_random_workspace()
workspace_item3 = ObjMother.generate_random_workspace_item(workspace=workspace3)
diagram3 = ObjMother.generate_random_diagram(workspace=workspace3)
persisted_item3 = ObjMother.generate_random_diagram_item(workspace_item=workspace_item3, diagram=diagram3)

persisted_item4 = ObjMother.generate_random_diagram_item()

user_access = list()
user_access.append(UserAccess(workspace=workspace2, permission=UserPermission.EDIT))
user_access.append(UserAccess(workspace=workspace3, permission=UserPermission.VIEW))
current_user.user_access = user_access


class TestDiagramItemService(unittest.TestCase):

    def setUp(self):
        self.diagram_item_repository = Mock()
        self.diagram_service = Mock()
        self.authentication_repository = Mock()
        self.workspace_item_service = Mock()

        self.diagram_item_service = DiagramItemService(self.diagram_item_repository, self.authentication_repository,
                                                       self.diagram_service, self.workspace_item_service)

        self.authentication_repository.get_current_user.return_value = current_user
        diagrams = [diagram1, diagram2, diagram3, diagram11]
        self.diagram_service.find_diagram_by_id = \
            Mock(side_effect=lambda di_id, _: next((d for d in diagrams if d.id == di_id), None))

        diagram_items = [persisted_item1, persisted_item2, persisted_item3, persisted_item4]
        self.diagram_item_repository.find_by_id = \
            Mock(side_effect=lambda di_id: next((d for d in diagram_items if d.id == di_id), None))
        self.diagram_item_repository.find_all_by_diagram = \
            Mock(side_effect=lambda diagram: [d for d in diagram_items if d.diagram.id == diagram.id])

    def test_create_item_diagram_success(self):
        # given
        diagram_item = ObjMother.generate_random_diagram_item(workspace_item=workspace_item1, diagram=diagram1)

        # when
        self.diagram_item_service.create_diagram_item(diagram_item)

        # then
        self.diagram_item_repository.create.assert_called_with(diagram_item)

    @parameterized.expand([
        (DiagramItem(id=None, workspace_item=None, diagram=diagram1), ["workspace_item"]),
        (DiagramItem(id=None, workspace_item=workspace_item1, diagram=None), ["diagram"]),
        (DiagramItem(id=None, workspace_item=workspace_item1, diagram=diagram3), ["workspace_item"])
    ])
    def test_create_item_diagram_missing_fields(self, diagram_item: DiagramItem, missing_fields: List[str]):

        # when
        with self.assertRaises(InvalidEntityException) as exception_context:
            self.diagram_item_service.create_diagram_item(diagram_item)

        # then
        self.diagram_item_repository.create.assert_not_called()
        self.assertEqual(missing_fields, exception_context.exception.missing_fields)

    def test_update_diagram_item_success(self):
        # given
        diagram_item = deepcopy(persisted_item1)
        persisted_item1.workspace_item = workspace_item11

        # when
        self.diagram_item_service.update_diagram_item(diagram_item)

        # then
        self.diagram_item_repository.update.assert_called_with(diagram_item)

    @parameterized.expand([
        (DiagramItem(id=persisted_item1.id, workspace_item=None, diagram=diagram1), ["workspace_item"]),
        (DiagramItem(id=persisted_item1.id, workspace_item=workspace_item1, diagram=None), ["diagram"]),
        (DiagramItem(id=persisted_item3.id, workspace_item=workspace_item1, diagram=diagram3), ["workspace_item"]),
        (DiagramItem(id=persisted_item1.id, workspace_item=workspace_item1, diagram=diagram11), ["diagram"])
    ])
    def test_update_diagram_item_without_required_fields(self, diagram_item: DiagramItem, missing_fields: List[str]):
        # when
        with self.assertRaises(InvalidEntityException) as exception_context:
            self.diagram_item_service.update_diagram_item(diagram_item)

        # then
        self.assertEqual(missing_fields, exception_context.exception.missing_fields)

    @parameterized.expand([
        (persisted_item1,),
        (persisted_item2,)
    ])
    def test_delete_diagram_item_success(self, diagram_item: DiagramItem):
        # given
        diagram_item_id = diagram_item.id

        # when
        self.diagram_item_service.delete_diagram_item(diagram_item_id)

        # then
        self.diagram_item_repository.delete.assert_called_with(diagram_item_id)

    @parameterized.expand([
        (persisted_item3,),
        (persisted_item4,)
    ])
    def test_delete_diagram_item_without_permission(self, diagram_item: DiagramItem):
        # given
        diagram_item_id = diagram_item.id

        # when
        self.assertRaises(PermissionException, self.diagram_item_service.delete_diagram_item, diagram_item_id)

        # then
        self.diagram_item_repository.delete.assert_not_called()

    def teste_delete_not_persisted_diagram_item(self):
        # given
        diagram_item_id = uuid4()

        # when
        self.assertRaises(EntityNotFoundException, self.diagram_item_service.delete_diagram_item, diagram_item_id)

        # then
        self.diagram_item_repository.assert_not_called()

    @parameterized.expand([
        (persisted_item1,),
        (persisted_item2,),
        (persisted_item3,)
    ])
    def test_find_diagram_item_by_id_with_success(self, diagram_item: DiagramItem):
        # given
        diagram_item_id = diagram_item.id

        # when
        diagram_item = self.diagram_item_service.find_diagram_item_by_id(diagram_item_id)

        # then
        self.assertEqual(diagram_item_id, diagram_item.id)

    def test_find_diagram_item_by_id_without_permission(self):
        # given
        diagram_item_id = persisted_item4.id

        # when/then
        self.assertRaises(PermissionException, self.diagram_item_service.find_diagram_item_by_id, diagram_item_id)

    def test_find_diagram_item_by_id_without_item(self):
        # given
        diagram_item_id = uuid4()

        # when/then
        self.assertRaises(EntityNotFoundException, self.diagram_item_service.find_diagram_item_by_id, diagram_item_id)

    @parameterized.expand([
        (diagram1,),
        (diagram2,),
        (diagram3,)
    ])
    def test_find_items_by_diagram_with_success(self, diagram: Diagram):
        # given
        diagram_id = diagram.id

        # when
        diagram_items = self.diagram_item_service.find_diagram_items_by_diagram(diagram_id)

        # then
        self.assertEqual(1, len(diagram_items))

    def test_find_items_by_diagram_without_permission(self):
        # given
        diagram_id = persisted_item4.diagram.id
        self.diagram_service.find_diagram_by_id = Mock(side_effect=PermissionException("Diagram", diagram_id,
                                                                                       current_user))

        # when/then
        self.assertRaises(PermissionException, self.diagram_item_service.find_diagram_items_by_diagram, diagram_id)
