import unittest
from copy import deepcopy
from typing import List
from unittest.mock import Mock
from uuid import uuid4

from parameterized import parameterized

from c4maker_server.domain.entities.diagram import Diagram, DiagramType
from c4maker_server.domain.entities.user_access import UserAccess, UserPermission
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.diagram_service import DiagramService
from tests.utils.obj_mother import ObjMother

current_user = ObjMother.generate_random_user()
workspace1 = ObjMother.generate_random_workspace(user=current_user)
persisted_diagram1 = ObjMother.generate_random_diagram(workspace=workspace1)
persisted_diagram2 = ObjMother.generate_random_diagram(workspace=workspace1)

workspace2 = ObjMother.generate_random_workspace()
persisted_diagram3 = ObjMother.generate_random_diagram(workspace=workspace2)

workspace3 = ObjMother.generate_random_workspace()
persisted_diagram4 = ObjMother.generate_random_diagram(workspace=workspace3)

workspace4 = ObjMother.generate_random_workspace()
persisted_diagram5 = ObjMother.generate_random_diagram(workspace=workspace4)

user_access = list()
user_access.append(UserAccess(workspace=workspace2, permission=UserPermission.EDIT))
user_access.append(UserAccess(workspace=workspace3, permission=UserPermission.VIEW))
current_user.user_access = user_access


class TestDiagramService(unittest.TestCase):

    def setUp(self):
        self.diagram_repository = Mock()
        self.authentication_repository = Mock()
        self.workspace_servie = Mock()
        self.diagram_service = DiagramService(self.diagram_repository, self.authentication_repository,
                                              self.workspace_servie)

        self.authentication_repository.get_current_user.return_value = current_user

        diagrams = [persisted_diagram1, persisted_diagram2, persisted_diagram3, persisted_diagram4, persisted_diagram5]

        self.diagram_repository.find_by_id = \
            Mock(side_effect=lambda diagram_id: next((d for d in diagrams if d.id == diagram_id), None))

    @parameterized.expand([
        (Diagram(id=None, name="Diagram 1", description="Desc", workspace=workspace1, diagram_type=DiagramType.C4),),
        (Diagram(id=None, name="Diagram 1", description=None, workspace=workspace1, diagram_type=DiagramType.TEXT),)
    ])
    def test_create_diagram_success(self, diagram: Diagram):

        # when
        self.diagram_service.create_diagram(diagram)

        # then
        self.diagram_repository.create.assert_called_with(diagram)
        self.assertIsNotNone(diagram.created_by)
        self.assertIsNotNone(diagram.created_at)
        self.assertIsNotNone(diagram.modified_by)
        self.assertIsNotNone(diagram.modified_at)

    @parameterized.expand([
        (Diagram(id=None, name=None, description="Desc", workspace=workspace1, diagram_type=DiagramType.C4), ["name"]),
        (Diagram(id=None, name="name", description="Desc", workspace=None, diagram_type=DiagramType.C4), ["workspace"]),
        (Diagram(id=None, name="name", description="Desc", workspace=workspace1, diagram_type=None), ["diagram_type"])
    ])
    def test_create_diagram_without_required_fields(self, diagram: Diagram, missing_fields: List[str]):

        # when
        with self.assertRaises(InvalidEntityException) as exception_context:
            self.diagram_service.create_diagram(diagram)

        self.diagram_repository.create.assert_not_called()
        self.assertEqual(missing_fields, exception_context.exception.missing_fields)

    def test_create_diagram_without_workspace_permission(self):
        # given
        diagram = Diagram(id=None, name="name", description="Desc", workspace=workspace4, diagram_type=DiagramType.C4)

        # when
        self.assertRaises(PermissionException, self.diagram_service.create_diagram, diagram)

        # then
        self.diagram_repository.create.assert_not_called()

    @parameterized.expand([
        (persisted_diagram1,),
        (persisted_diagram2,),
        (persisted_diagram3,)
    ])
    def test_update_diagram_success(self, diagram: Diagram):
        # given
        new_name = "new name"
        new_description = "new description"
        diagram = deepcopy(diagram)
        diagram.name = new_name
        diagram.description = new_description

        # when
        self.diagram_service.update_diagram(diagram)

        # then
        self.diagram_repository.update.assert_called_with(diagram)
        self.assertEqual(new_name, diagram.name)
        self.assertEqual(new_description, diagram.description)
        self.assertEqual(current_user, diagram.modified_by)
        self.assertIsNotNone(diagram.modified_at)

    @parameterized.expand([
        (persisted_diagram4,),
        (persisted_diagram5,)
    ])
    def test_update_diagram_without_permission(self, diagram: Diagram):
        # given
        new_name = "new name"
        new_description = "new description"
        diagram = deepcopy(diagram)
        diagram.name = new_name
        diagram.description = new_description

        # when / then
        self.assertRaises(PermissionException, self.diagram_service.update_diagram, diagram)

        # then
        self.diagram_repository.update.assert_not_called()

    def test_update_diagram_not_found_failed(self):
        # given
        diagram = deepcopy(persisted_diagram1)
        diagram.id = uuid4()

        with self.assertRaises(EntityNotFoundException):
            self.diagram_service.update_diagram(diagram)

        self.diagram_repository.update.assert_not_called()

    @parameterized.expand([
        (Diagram(id=persisted_diagram1.id, name=None, description="Desc", workspace=workspace1,
                 diagram_type=DiagramType.C4), ["name"]),
        (Diagram(id=persisted_diagram2.id, name="name", description="Desc", workspace=None,
                 diagram_type=DiagramType.C4), ["workspace"]),
        (Diagram(id=persisted_diagram3.id, name="name", description="Desc", workspace=workspace2,
                 diagram_type=None), ["diagram_type"])
    ])
    def test_update_diagram_without_required_fields(self, diagram: Diagram, missing_fields: List[str]):

        # when
        with self.assertRaises(InvalidEntityException) as exception_context:
            self.diagram_service.update_diagram(diagram)

        self.diagram_repository.update.assert_not_called()
        self.assertEqual(missing_fields, exception_context.exception.missing_fields)

    def test_update_diagram_changing_workspace(self):
        # given
        diagram = deepcopy(persisted_diagram1)
        diagram.workspace = workspace2

        # when
        self.assertRaises(InvalidEntityException, self.diagram_service.update_diagram, diagram)

        # then
        self.diagram_repository.update.assert_not_called()

    @parameterized.expand([
        (persisted_diagram1,),
        (persisted_diagram2,),
        (persisted_diagram3,)
    ])
    def test_delete_diagram_success(self, diagram: Diagram):
        # given
        diagram_id = diagram.id

        # when
        self.diagram_service.delete_diagram(diagram_id)

        # then
        self.diagram_repository.delete.assert_called_with(diagram_id)

    @parameterized.expand([
        (persisted_diagram4,),
        (persisted_diagram5,)
    ])
    def test_delete_without_permission(self, diagram: Diagram):
        # given
        diagram_id = diagram.id

        # when
        self.assertRaises(PermissionException, self.diagram_service.delete_diagram, diagram_id)

        # then
        self.diagram_repository.delete.assert_not_called()

    def test_delete_not_found_permission(self):
        # given
        diagram_id = uuid4()

        # when
        self.assertRaises(EntityNotFoundException, self.diagram_service.delete_diagram, diagram_id)

        # then
        self.diagram_repository.delete.assert_not_called()

    @parameterized.expand([
        (persisted_diagram1,),
        (persisted_diagram2,),
        (persisted_diagram3,)
    ])
    def test_find_by_id_with_success(self, diagram: Diagram):
        # given
        diagram_id = diagram.id

        # when
        diagram = self.diagram_service.find_diagram_by_id(diagram_id)

        # then
        self.assertEqual(diagram_id, diagram.id)
        self.assertIsNotNone(diagram.name)
        self.assertIsNotNone(diagram.description)
        self.assertIsNotNone(diagram.workspace)
        self.assertIsNotNone(diagram.diagram_type)
