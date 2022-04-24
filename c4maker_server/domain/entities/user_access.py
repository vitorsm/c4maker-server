import enum
from dataclasses import dataclass

from c4maker_server.domain.entities.diagram import Diagram


class UserPermission(enum.Enum):
    VIEW = 1
    EDIT = 2


@dataclass
class UserAccess:
    diagram: Diagram
    permission: UserPermission

    @staticmethod
    def instantiate_permission_by_name(permission_name: str) -> UserPermission:
        user_permissions = list(map(lambda p: p, UserPermission))
        return next((p for p in user_permissions if p.name == permission_name), None)
