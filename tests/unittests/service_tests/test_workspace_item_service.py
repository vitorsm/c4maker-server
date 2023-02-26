import unittest
from copy import deepcopy
from typing import List
from unittest.mock import Mock

from parameterized import parameterized

from c4maker_server.domain.entities.user_access import UserAccess, UserPermission
from c4maker_server.domain.entities.workspace_item import WorkspaceItem, WorkspaceItemType
from c4maker_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from c4maker_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from c4maker_server.domain.exceptions.permission_exception import PermissionException
from c4maker_server.services.workspace_item_service import WorkspaceItemService
from tests.utils.obj_mother import ObjMother

current_user = ObjMother.generate_random_user()

workspace1 = ObjMother.generate_random_workspace(user=current_user)
persisted_item1 = ObjMother.generate_random_workspace_item(workspace=workspace1)

workspace2 = ObjMother.generate_random_workspace()
persisted_item2 = ObjMother.generate_random_workspace_item(workspace=workspace2)

workspace3 = ObjMother.generate_random_workspace()
persisted_item3 = ObjMother.generate_random_workspace_item(workspace=workspace3)

persisted_item4 = ObjMother.generate_random_workspace_item()

user_access = list()
user_access.append(UserAccess(workspace=workspace2, permission=UserPermission.EDIT))
user_access.append(UserAccess(workspace=workspace3, permission=UserPermission.VIEW))
current_user.user_access = user_access


class TestWorkspaceItemService(unittest.TestCase):

    def setUp(self):
        self.workspace_item_repository = Mock()
        self.authentication_repository = Mock()
        self.workspace_service = Mock()

        self.workspace_item_service = WorkspaceItemService(self.workspace_item_repository,
                                                           self.authentication_repository, self.workspace_service)

        self.authentication_repository.get_current_user.return_value = current_user

        workspaces = [workspace1, workspace2, workspace3]
        self.workspace_service.find_workspace_by_id = \
            Mock(side_effect=lambda w_id, _: next((w for w in workspaces if w.id == w_id), None))

        workspace_items = [persisted_item1, persisted_item2, persisted_item3, persisted_item4]
        self.workspace_item_repository.find_by_id = \
            Mock(side_effect=lambda wi_id: next((w for w in workspace_items if w.id == wi_id), None))

    def test_create_or_update_with_create(self):
        # given
        workspace_item = ObjMother.generate_random_workspace_item(workspace=workspace1)
        workspace_item.id = None

        # when
        self.workspace_item_service.create_or_update_workspace_item(workspace_item)

        # then
        self.workspace_item_repository.create.assert_called_with(workspace_item)
        self.workspace_item_repository.update.assert_not_called()

    def test_create_or_update_with_update(self):
        # given
        workspace_item = deepcopy(persisted_item1)
        workspace_item.name = "new name"

        # when
        self.workspace_item_service.create_or_update_workspace_item(workspace_item)

        # then
        self.workspace_item_repository.create.assert_not_called()
        self.workspace_item_repository.update.assert_called_with(workspace_item)

    def test_create_workspace_item_with_success(self):
        # given
        workspace_item = ObjMother.generate_random_workspace_item(workspace=workspace1)
        workspace_item.id = None

        # when
        self.workspace_item_service.create_workspace_item(workspace_item)

        # then
        self.workspace_item_repository.create.assert_called_with(workspace_item)
        self.assertIsNotNone(workspace_item.created_at)
        self.assertIsNotNone(workspace_item.modified_at)
        self.assertIsNotNone(workspace_item.created_by)
        self.assertIsNotNone(workspace_item.modified_by)

    @parameterized.expand([
        (WorkspaceItem(id=None, workspace=workspace1, workspace_item_type=WorkspaceItemType.PERSONA, key="key",
                       name="", description="desc", details="det"), ["name"]),
        (WorkspaceItem(id=None, workspace=None, workspace_item_type=WorkspaceItemType.PERSONA, key="key",
                       name="name", description="desc", details="det"), ["workspace"]),
        (WorkspaceItem(id=None, workspace=workspace2, workspace_item_type=None, key="key",
                       name="name", description="desc", details="det"), ["workspace_item_type"]),
        (WorkspaceItem(id=None, workspace=workspace2, workspace_item_type=WorkspaceItemType.ENTITY, key="",
                       name="name", description="desc", details="det"), ["key"])
    ])
    def test_create_workspace_item_without_required_fields(self, workspace_item: WorkspaceItem,
                                                           missing_fields: List[str]):
        # when
        with self.assertRaises(InvalidEntityException) as exception_context:
            self.workspace_item_service.create_workspace_item(workspace_item)

        # then
        self.workspace_item_repository.create.assert_not_called()
        self.assertEqual(missing_fields, exception_context.exception.missing_fields)

    def test_create_workspace_item_without_workspace_permission(self):
        # given
        workspace_item = deepcopy(persisted_item4)
        workspace_item.id = None

        # when
        self.assertRaises(InvalidEntityException, self.workspace_item_service.create_workspace_item, workspace_item)

        # then
        self.workspace_item_repository.create.assert_not_called()

    @parameterized.expand([
        (persisted_item1,),
        (persisted_item2,)
    ])
    def test_update_workspace_item_with_success(self, workspace_item: WorkspaceItem):
        # given
        workspace_item = deepcopy(workspace_item)
        workspace_item.name = "new name"

        # when
        self.workspace_item_service.update_workspace_item(workspace_item)

        # then
        self.workspace_item_repository.update.assert_called_with(workspace_item)
        self.assertEqual(current_user, workspace_item.modified_by)
        self.assertIsNotNone(workspace_item.modified_at)

    def test_update_not_found(self):
        # given
        workspace_item = ObjMother.generate_random_workspace_item(workspace=workspace1)

        # when
        self.assertRaises(EntityNotFoundException, self.workspace_item_service.update_workspace_item, workspace_item)

        # then
        self.workspace_item_repository.update.assert_not_called()

    @parameterized.expand([
        (WorkspaceItem(id=persisted_item1.id, workspace=workspace1, workspace_item_type=WorkspaceItemType.PERSONA,
                       key="key", name="", description="desc", details="det"), ["name"]),
        (WorkspaceItem(id=persisted_item1.id, workspace=None, workspace_item_type=WorkspaceItemType.PERSONA, key="key",
                       name="name", description="desc", details="det"), ["workspace"]),
        (WorkspaceItem(id=persisted_item2.id, workspace=workspace2, workspace_item_type=None, key="key",
                       name="name", description="desc", details="det"), ["workspace_item_type"]),
        (WorkspaceItem(id=persisted_item2.id, workspace=workspace2, workspace_item_type=WorkspaceItemType.ENTITY,
                       key="", name="name", description="desc", details="det"), ["key"])
    ])
    def test_update_workspace_item_without_required_fields(self, workspace_item: WorkspaceItem,
                                                           missing_fields: List[str]):

        # when
        with self.assertRaises(InvalidEntityException) as exception_context:
            self.workspace_item_service.update_workspace_item(workspace_item)

        # then
        self.workspace_item_repository.update.assert_not_called()
        self.assertEqual(missing_fields, exception_context.exception.missing_fields)

    def test_update_workspace_item_changing_workspace(self):
        # given
        workspace_item = deepcopy(persisted_item1)
        workspace_item.workspace = workspace2

        # when
        self.assertRaises(InvalidEntityException, self.workspace_item_service.update_workspace_item, workspace_item)

        # then
        self.workspace_item_repository.update.assert_not_called()

    @parameterized.expand([
        (persisted_item1,),
        (persisted_item2,)
    ])
    def test_delete_workspace_item_with_success(self, workspace_item: WorkspaceItem):
        # given
        workspace_item_id = workspace_item.id

        # when
        self.workspace_item_service.delete_workspace_item(workspace_item_id)

        # then
        self.workspace_item_repository.delete.assert_called_with(workspace_item_id)

    @parameterized.expand([
        (persisted_item3,),
        (persisted_item4,)
    ])
    def test_delete_without_permission(self, workspace_item: WorkspaceItem):
        # given
        workspace_item_id = workspace_item.id

        # when
        self.assertRaises(PermissionException, self.workspace_item_service.delete_workspace_item, workspace_item_id)

        # then
        self.workspace_item_repository.delete.assert_not_called()

    @parameterized.expand([
        (persisted_item1,),
        (persisted_item2,),
        (persisted_item3,)
    ])
    def test_find_workspace_item_by_id_with_success(self, workspace_item: WorkspaceItem):
        # given
        workspace_item_id = workspace_item.id

        # when
        workspace_item = self.workspace_item_service.find_workspace_item_by_id(workspace_item_id)

        # then
        self.assertEqual(workspace_item_id, workspace_item.id)
        self.assertIsNotNone(workspace_item.name)
        self.assertIsNotNone(workspace_item.workspace)
        self.assertIsNotNone(workspace_item.key)
        self.assertIsNotNone(workspace_item.details)
        self.assertIsNotNone(workspace_item.description)

    def test_find_workspace_item_by_id_without_permission(self):
        # given
        workspace_item_id = persisted_item4.id

        # when/then
        self.assertRaises(PermissionException, self.workspace_item_service.find_workspace_item_by_id, workspace_item_id)
