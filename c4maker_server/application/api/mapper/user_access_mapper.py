from typing import Optional

from c4maker_server.application.api.mapper.diagram_mapper import DiagramMapper
from c4maker_server.domain.entities.user_access import UserAccess


class UserAccessMapper:

    @staticmethod
    def to_entity(user_access_dto: dict) -> Optional[UserAccess]:
        if not user_access_dto:
            return None

        return UserAccess(diagram=DiagramMapper.to_entity(user_access_dto.get("diagram")),
                          permission=UserAccess.instantiate_permission_by_name(user_access_dto.get("permission")))

    @staticmethod
    def to_dto(user_access: UserAccess) -> Optional[dict]:
        if not user_access:
            return None

        return {
            "permission": user_access.permission.name,
            "diagram": DiagramMapper.to_dto(user_access.diagram)
        }
