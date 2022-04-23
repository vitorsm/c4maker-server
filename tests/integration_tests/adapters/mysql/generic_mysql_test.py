import abc
from typing import Any
from uuid import uuid4

from c4maker_server.domain.exceptions.duplicate_entity_exception import DuplicateEntityException
from tests.integration_tests.base_integ_test import BaseIntegTest


class GenericMySQLTest(BaseIntegTest, metaclass=abc.ABCMeta):

    def setUp(self):
        self.create_app()
        super().setUp()
        self.repository = self.get_repository()

    @abc.abstractmethod
    def get_repository(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_default_entity(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_updated_default_entity(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_entity_name(self) -> str:
        raise NotImplementedError

    def get_new_entity_by_default(self) -> Any:
        default_entity = self.get_default_entity()
        default_entity.id = uuid4()

        return default_entity

    def compare_obj_properties(self, obj1: Any, obj2: Any):
        dict1 = obj1.__dict__
        dict2 = obj2.__dict__

        for key1, value1 in dict1.items():
            value2 = dict2.get(key1)
            self.assertEqual(value1, value2, f"value expected for {key1} is value1 but has {value2}")

    def test_find_entity(self):
        # given
        default_entity = self.get_default_entity()

        # when
        persisted_entity = self.repository.find_by_id(self.DEFAULT_ID)

        # then
        self.compare_obj_properties(default_entity, persisted_entity)

    def test_find_entity_not_found(self):
        # given
        not_existing_id = uuid4()

        # when
        entity = self.repository.find_by_id(not_existing_id)

        # then
        self.assertIsNone(entity)

    def test_create_entity(self):
        # given
        new_entity = self.get_new_entity_by_default()
        self.repository.create(new_entity)

        # when
        persisted_entity = self.repository.find_by_id(new_entity.id)

        # then
        self.compare_obj_properties(new_entity, persisted_entity)

    def test_create_duplicate_entity(self):
        # given
        default_entity = self.get_default_entity()

        # when
        with self.assertRaises(DuplicateEntityException) as ex_context:
            self.repository.create(default_entity)

        # then
        self.assertEqual(f"The {self.get_entity_name()} {default_entity.id} is already persisted",
                         str(ex_context.exception))

    def test_update_entity(self):
        entity = self.repository.find_by_id(self.DEFAULT_ID)
        # ensuring that entity exists and match with default entity
        self.compare_obj_properties(self.get_default_entity(), entity)

        # given
        updated_entity = self.get_updated_default_entity()
        self.repository.update(updated_entity)

        # when
        persisted_entity = self.repository.find_by_id(self.DEFAULT_ID)

        # then
        self.compare_obj_properties(updated_entity, persisted_entity)

    def test_delete_entity(self):
        # given
        entity = self.repository.find_by_id(self.DEFAULT_ID)
        # ensuring that entity exists
        self.assertIsNotNone(entity)

        # when
        self.repository.delete(self.DEFAULT_ID)

        # then
        entity = self.repository.find_by_id(self.DEFAULT_ID)
        self.assertIsNone(entity)

    def test_delete_non_exists_entity(self):
        # nothing is expected. Just to test behaviour
        self.repository.delete(uuid4())
