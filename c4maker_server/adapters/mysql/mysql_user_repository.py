from typing import Optional
from uuid import UUID

from c4maker_server.adapters.models import UserDB
from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.domain.entities.user import User
from c4maker_server.services.ports.user_repository import UserRepository


class MySQLUserRepository(UserRepository):

    def __init__(self, mysql_client: MySQLClient):
        self.mysql_client = mysql_client

    def create_user(self, user: User):
        user_db = UserDB(user)
        self.mysql_client.add(user_db)

    def find_by_id(self, user_id: UUID, reduced: bool = True) -> Optional[User]:
        user_db = self.mysql_client.db.session.query(UserDB).get(str(user_id))

        if not user_db:
            return None

        return user_db.to_entity(reduced)

    def find_by_login(self, login: str) -> Optional[User]:
        users_db = self.mysql_client.db.session.query(UserDB).filter(UserDB.login == login)

        if not users_db:
            return None

        try:
            return users_db[0].to_entity()
        except IndexError:
            return None
