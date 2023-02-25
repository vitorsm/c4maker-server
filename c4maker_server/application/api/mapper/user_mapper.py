from typing import Optional

from c4maker_server.application.api.mapper.reduced_user_mapper import ReducedUserMapper
from c4maker_server.application.api.mapper.user_access_mapper import UserAccessMapper
from c4maker_server.domain.entities.user import User


class UserMapper:

    @staticmethod
    def to_entity(user_dto: dict) -> Optional[User]:
        if not user_dto:
            return None
        user = ReducedUserMapper.to_entity(user_dto)

        user.shared_diagrams = [UserAccessMapper.to_entity(d) for d in user_dto.get("user_access", [])]

        return user

    @staticmethod
    def to_dto(user: User) -> Optional[dict]:
        if not user:
            return None

        user_dto = ReducedUserMapper.to_dto(user)

        user_dto["user_access"] = [UserAccessMapper.to_dto(d) for d in user.user_access]

        return user_dto
