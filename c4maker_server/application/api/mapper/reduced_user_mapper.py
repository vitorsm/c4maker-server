from typing import Optional
from uuid import UUID

from c4maker_server.domain.entities.user import User
from c4maker_server.utils import utils


class ReducedUserMapper:

    @staticmethod
    def to_entity(user_dto: dict) -> Optional[User]:
        if not user_dto:
            return None

        user = User(id=utils.str_to_uuid(user_dto.get("id")), name=user_dto.get("name"), login=user_dto.get("login"),
                    password=user_dto.get("password"), shared_diagrams=list())

        return user

    @staticmethod
    def to_dto(user: User) -> Optional[dict]:
        if not user:
            return None

        user_dto = {
            "id": str(user.id),
            "name": user.name,
            "login": user.login,
            "password": None
        }

        return user_dto
