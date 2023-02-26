import uuid

from c4maker_server.adapters.mysql.mysql_user_repository import MySQLUserRepository
from c4maker_server.domain.exceptions.duplicate_entity_exception import DuplicateEntityException
from tests.integration_tests.adapters.mysql.generic_mysql_test import GenericMySQLTest
from tests.integration_tests.base_integ_test import BaseIntegTest
from tests.integration_tests.default_values import DefaultValues


class TestMySQLUserRepository(BaseIntegTest):
    repository: MySQLUserRepository = None

    def setUp(self):
        super().setUp()
        self.repository = MySQLUserRepository(self.mysql_client)

    def get_test_case(self):
        return self

    def test_create_user(self):
        # given
        new_user = DefaultValues.get_default_user()
        new_user.id = uuid.uuid4()
        new_user.login = "new_login"
        self.repository.create(new_user)

        # when
        persisted_entity = self.repository.find_by_id(new_user.id)

        # then
        GenericMySQLTest.compare_obj_properties(self, new_user, persisted_entity)

    def test_create_duplicate_user_by_id(self):
        # given
        new_user = DefaultValues.get_default_user()
        new_user.login = "new_login"

        # when
        with self.assertRaises(DuplicateEntityException) as ex_context:
            self.repository.create(new_user)

        # then
        self.assertEqual(f"The User {new_user.id} is already persisted", str(ex_context.exception))

    def test_create_duplicate_user_by_login(self):
        # given
        new_user = DefaultValues.get_default_user()
        new_user.id = uuid.uuid4()

        # when
        with self.assertRaises(DuplicateEntityException) as ex_context:
            self.repository.create(new_user)

        # then
        self.assertEqual(f"The User {new_user.login} is already persisted", str(ex_context.exception))

    def test_find_user(self):
        # given
        default_user = DefaultValues.get_default_user()

        # when
        persisted_user = self.repository.find_by_id(DefaultValues.DEFAULT_ID)

        # then
        GenericMySQLTest.compare_obj_properties(self, default_user, persisted_user)

    def test_find_user_by_login(self):
        # given
        default_user = DefaultValues.get_default_user()

        # when
        persisted_user = self.repository.find_by_login(default_user.login)

        # then
        GenericMySQLTest.compare_obj_properties(self, default_user, persisted_user)

    def test_find_entity_not_found(self):
        # given
        not_existing_id = uuid.uuid4()

        # when
        entity = self.repository.find_by_id(not_existing_id)

        # then
        self.assertIsNone(entity)

    def test_find_entity_not_found_by_login(self):
        # given
        not_existing_login = "not_existing_id"

        # when
        entity = self.repository.find_by_login(not_existing_login)

        # then
        self.assertIsNone(entity)
