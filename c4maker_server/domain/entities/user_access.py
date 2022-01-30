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

