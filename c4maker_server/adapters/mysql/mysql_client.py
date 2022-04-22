from typing import Any

from sqlalchemy.exc import IntegrityError

from c4maker_server.domain.exceptions.duplicate_entity_exception import DuplicateEntityException
from c4maker_server.utils import sql_utils


class MySQLClient:
    def __init__(self, db):
        self.db = db

    def add(self, entity: Any, commit: bool = True):
        self.db.session.add(entity)
        if commit:
            try:
                self.__commit(raise_integrity_error=True)
            except IntegrityError as ex:
                self.__handle_integrity_error(ex, type(entity).__name__)

    def update(self, entity: Any, commit: bool = True):
        if entity not in self.db.session:
            self.db.session.add(entity)
        if commit:
            self.db.session.commit()

    def delete(self, entity: Any, commit: bool = True):
        self.db.session.delete(entity)
        if commit:
            self.__commit()

    def __commit(self, raise_integrity_error: bool = False):
        try:
            self.db.session.commit()
        except IntegrityError as ex:
            if raise_integrity_error:
                raise ex
            else:
                self.__handle_integrity_error(ex, "")

    @staticmethod
    def __handle_integrity_error(exception: IntegrityError, entity: str):
        if "UNIQUE" in exception.args[0] or "Duplicate" in exception.args[0]:
            if "UNIQUE" in exception.args[0]:
                field = exception.args[0].split(': ')[1]
            else:
                field = exception.args[0].split('\' for key \'')[1][:-3].split('.')[1]
            value = None

            if "." in field:
                field = field.split(".")[1]

            index = sql_utils.get_position_of_field_in_insert_query(exception.statement, field)

            if exception.params and len(exception.params) > index >= 0:
                if type(exception.params) == list or type(exception.params) == tuple:
                    value = exception.params[index]
                else:
                    value = exception.params[field]

            raise DuplicateEntityException(entity, value)

        raise exception
