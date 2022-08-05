import abc
import json
from typing import Any, Optional, Union

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class GenericControllerTest(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def _get_endpoint(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_endpoint_by_id(self, entity_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_invalid_insert_payload(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_insert_payload(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_client(self) -> FlaskClient:
        raise NotImplementedError

    @abc.abstractmethod
    def get_authentication_header(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_authentication_header_without_permission(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_default_id(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_not_persisted_id(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def assertEqual(self, expected_value, actual_value):
        raise NotImplementedError

    @abc.abstractmethod
    def assertIsNotNone(self, value):
        raise NotImplementedError

    def __get_header(self, with_auth: bool, with_token_no_permission: bool) -> Optional[dict]:
        header = None
        if not with_auth:
            return header

        if with_token_no_permission:
            header = self.get_authentication_header_without_permission()
        else:
            header = self.get_authentication_header()

        return header

    def _get_items(self, with_auth: bool = True, with_token_no_permission: bool = False) -> TestResponse:
        return self.get_client().get(self._get_endpoint(), headers=self.__get_header(with_auth,
                                                                                     with_token_no_permission))

    def _get_item_by_id(self, entity_id: str, with_auth: bool = True,
                        with_token_no_permission: bool = False) -> TestResponse:
        return self.get_client().get(self._get_endpoint_by_id(entity_id),
                                     headers=self.__get_header(with_auth, with_token_no_permission))

    def _post_item(self, payload: dict, with_auth: bool = True, with_token_no_permission: bool = False) -> TestResponse:
        return self.get_client().post(self._get_endpoint(), json=payload,
                                      headers=self.__get_header(with_auth, with_token_no_permission))

    def _put_item(self, payload: dict, with_auth: bool = True, with_token_no_permission: bool = False) -> TestResponse:
        return self.get_client().put(f"{self._get_endpoint()}/{payload['id']}", json=payload,
                                     headers=self.__get_header(with_auth, with_token_no_permission))

    def _delete_item(self, entity_id: str, with_auth: bool = True,
                     with_token_no_permission: bool = False) -> TestResponse:
        return self.get_client().delete(self._get_endpoint_by_id(entity_id),
                                        headers=self.__get_header(with_auth, with_token_no_permission))
    
    def test_find_item_by_id(self):
        response = self._get_item_by_id(self.get_default_id())

        response_dto = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        self.__assert_each_item(response_dto)
        self.assertEqual(self.get_default_id(), response_dto["id"])

    def test_not_found_item_by_id(self):
        response = self._get_item_by_id(self.get_not_persisted_id())
        self.assertEqual(404, response.status_code)

    def test_not_authenticate_get_item_by_id(self):
        response = self._get_item_by_id(self.get_default_id(), with_auth=False)
        self.assertEqual(401, response.status_code)

    def test_find_all_items(self):
        response = self._get_items()

        response_dto = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        self.__assert_each_item(response_dto)
        self.assertEqual(self.get_default_id(), response_dto[0]["id"])
        self.assertEqual(2, len(response_dto))

    def test_not_authenticate_find_all_items(self):
        response = self._get_items(with_auth=False)
        self.assertEqual(401, response.status_code)

    def test_insert_item(self):
        response = self._post_item(self._get_insert_payload())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(201, response.status_code)
        self.__assert_each_item(response_dto)
        self.__assert_dicts(self._get_insert_payload(), response_dto)

        response = self._get_item_by_id(response_dto["id"])
        response_dto = json.loads(response.data.decode())
        self.__assert_each_item(response_dto)
        self.__assert_dicts(self._get_insert_payload(), response_dto)

    def test_not_authenticated_insert_item(self):
        response = self._post_item(self._get_insert_payload(), with_auth=False)
        self.assertEqual(401, response.status_code)

    def test_insert_invalid_item(self):
        response = self._post_item(self._get_invalid_insert_payload())
        self.assertEqual(400, response.status_code)

    def test_update_item(self):
        item_to_update = self._get_insert_payload()
        item_to_update["id"] = self.get_default_id()

        response = self._put_item(item_to_update)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.__assert_each_item(response_dto)
        self.__assert_dicts(self._get_insert_payload(), response_dto)

        response = self._get_item_by_id(response_dto["id"])
        response_dto = json.loads(response.data.decode())
        self.__assert_each_item(response_dto)
        self.__assert_dicts(self._get_insert_payload(), response_dto)

    def test_update_invalid_item(self):
        item_to_update = self._get_invalid_insert_payload()
        item_to_update["id"] = self.get_default_id()

        response = self._put_item(item_to_update)
        self.assertEqual(400, response.status_code)

    def test_not_authenticated_update_item(self):
        item_to_update = self._get_invalid_insert_payload()
        item_to_update["id"] = self.get_default_id()

        response = self._put_item(item_to_update, with_auth=False)
        self.assertEqual(401, response.status_code)

    def test_update_item_without_permission(self):
        item_to_update = self._get_invalid_insert_payload()
        item_to_update["id"] = self.get_default_id()

        response = self._put_item(item_to_update, with_token_no_permission=True)
        self.assertEqual(403, response.status_code)

    def test_delete_item(self):
        response = self._delete_item(self.get_default_id())
        self.assertEqual(200, response.status_code)

        response = self._get_item_by_id(self.get_default_id())
        self.assertEqual(404, response.status_code)

    def test_delete_item_not_found(self):
        response = self._delete_item(self.get_not_persisted_id())
        self.assertEqual(404, response.status_code)

    def test_delete_item_without_auth(self):
        response = self._delete_item(self.get_default_id(), with_auth=False)
        self.assertEqual(401, response.status_code)

    def test_delete_item_without_permission(self):
        response = self._delete_item(self.get_default_id(), with_token_no_permission=True)
        self.assertEqual(403, response.status_code)

    def __assert_dicts(self, item1: dict, item2: dict):
        for key, value in item1.items():
            self.assertEqual(value, item2.get(key))

    def __assert_each_item(self, item_dto: Union[dict, list]):
        if isinstance(item_dto, list):
            for item in item_dto:
                self.__assert_each_item(item)
        else:
            self.assertIsNotNone(item_dto["id"])
            self.assertIsNotNone(item_dto["name"])
            self.assertIsNotNone(item_dto["created_by"])
            self.assertIsNotNone(item_dto["created_at"])
            self.assertIsNotNone(item_dto["modified_at"])
