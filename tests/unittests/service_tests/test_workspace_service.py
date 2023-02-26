import unittest
import uuid
from copy import deepcopy
from unittest.mock import Mock

from parameterized import parameterized

from c4maker_server.domain.entities.user_access import UserAccess, UserPermission
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.workspace_service import WorkspaceService
from tests.utils.obj_mother import ObjMother

persisted_workspace1 = ObjMother.generate_random_workspace()
persisted_workspace2 = ObjMother.generate_random_workspace()
persisted_workspace3 = ObjMother.generate_random_workspace()

user_access = list()
user_access.append(UserAccess(workspace=persisted_workspace1, permission=UserPermission.EDIT))
user_access.append(UserAccess(workspace=persisted_workspace2, permission=UserPermission.VIEW))

current_user = ObjMother.generate_random_user(user_access=user_access)

persisted_workspace4 = ObjMother.generate_random_workspace(user=current_user)


class TestWorkspaceService(unittest.TestCase):
    def setUp(self):
        self.workspace_repository = Mock()
        self.authentication_repository = Mock()

        self.workspace_service = WorkspaceService(self.workspace_repository, self.authentication_repository)

        self.current_user = current_user
        self.authentication_repository.get_current_user = Mock(return_value=self.current_user)

        workspaces = [persisted_workspace1, persisted_workspace2, persisted_workspace3, persisted_workspace4]
        self.workspace_repository.find_by_id = \
            Mock(side_effect=
                 lambda workspace_id: next((w for w in workspaces if w.id == workspace_id), None))

    def test_create_workspace_with_success(self):
        workspace = Workspace(id=None, name="Workspace 1", description="desc 1")
        self.workspace_service.create_workspace(workspace)

        self.assertEqual(self.current_user, workspace.created_by)
        self.assertEqual(self.current_user, workspace.modified_by)
        self.assertIsNotNone(workspace.created_at)
        self.assertIsNotNone(workspace.modified_at)
        self.workspace_repository.create.assert_called_with(workspace)

    def test_create_workspace_without_required_fields(self):
        workspace = Workspace(id=None, name="", description="desc 1")

        with self.assertRaises(InvalidEntityException) as exception_context:
            self.workspace_service.create_workspace(workspace)

        self.workspace_repository.create.assert_not_called()
        self.assertIn("Workspace", str(exception_context.exception))
        self.assertEqual(["name"], exception_context.exception.missing_fields)

    @parameterized.expand([
        (persisted_workspace1,),
        (persisted_workspace4,)
    ])
    def test_update_workspace_with_success(self, workspace: Workspace):
        workspace = deepcopy(workspace)
        workspace.description = "Test"

        self.workspace_service.update_workspace(workspace)

        self.assertEqual(self.current_user, workspace.modified_by)
        self.assertIsNotNone(workspace.modified_at)
        self.workspace_repository.update.assert_called_with(workspace)

    @parameterized.expand([
        (persisted_workspace3,), (persisted_workspace2,)
    ])
    def test_update_workspace_without_permission(self, workspace: Workspace):
        workspace = deepcopy(workspace)
        workspace.description = "Test"

        self.assertRaises(PermissionException, self.workspace_service.update_workspace, workspace)
        self.workspace_repository.update.assert_not_called()

    def test_update_workspace_not_found(self):
        workspace = deepcopy(persisted_workspace1)
        workspace.id = uuid.uuid4()

        self.assertRaises(EntityNotFoundException, self.workspace_service.update_workspace, workspace)
        self.workspace_repository.update.assert_not_called()

    def test_update_workspace_without_required_fields(self):
        workspace = deepcopy(persisted_workspace1)
        workspace.name = None
        workspace.description = "new description"

        with self.assertRaises(InvalidEntityException) as exception_context:
            self.workspace_service.update_workspace(workspace)

        self.assertIn("Workspace", str(exception_context.exception))
        self.assertEqual(["name"], exception_context.exception.missing_fields)
        self.workspace_repository.update.assert_not_called()

    def test_delete_workspace(self):
        # given
        workspace_id = persisted_workspace4.id

        # when
        self.workspace_service.delete_workspace(workspace_id)

        # then
        self.workspace_repository.delete.assert_called_with(workspace_id)

    @parameterized.expand([
        (persisted_workspace1,), (persisted_workspace2,), (persisted_workspace3,)
    ])
    def test_delete_workspace_without_permission(self, workspace: Workspace):
        # given
        workspace_id = workspace.id

        # when
        self.assertRaises(PermissionException, self.workspace_service.delete_workspace, workspace_id)

        # then
        self.workspace_repository.delete.assert_not_called()

    def test_delete_workspace_without_persisted_workspace(self):
        # given
        workspace_id = uuid.uuid4()

        # when
        self.assertRaises(EntityNotFoundException, self.workspace_service.delete_workspace, workspace_id)

        # then
        self.workspace_repository.delete.assert_not_called()

    @parameterized.expand([
        (persisted_workspace1,), (persisted_workspace2,), (persisted_workspace4,)
    ])
    def test_find_workspace_by_id_with_success(self, workspace: Workspace):
        # given
        workspace_id = workspace.id

        # when
        workspace = self.workspace_service.find_workspace_by_id(workspace_id)

        # then
        self.assertEqual(workspace_id, workspace.id)

    def test_find_workspace_by_id_without_permission(self):
        # given
        workspace_id = persisted_workspace3.id

        # when / then
        self.assertRaises(PermissionException, self.workspace_service.find_workspace_by_id, workspace_id)
