from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.user_access import UserAccess, UserPermission


@dataclass
class User:
    id: UUID
    name: str
    login: str
    password: str
    shared_diagrams: List[UserAccess]

    def __eq__(self, other):
        return isinstance(other, User) and other.id == self.id

    @property
    def __dict__(self):
        if not hasattr(self, "id"):
            return {}

        return {
            "id": str(self.id),
            "name": self.name,
            "login": self.login
        }

    def is_owner(self, diagram: Diagram) -> bool:
        return diagram.created_by == self

    def allowed_to_edit(self, diagram: Diagram) -> bool:
        if self.is_owner(diagram):
            return True

        user_access = self.__get_user_access_by_diagram(diagram)

        if not user_access:
            return False

        return user_access.permission == UserPermission.EDIT

    def allowed_to_view(self, diagram: Diagram) -> bool:
        if self.is_owner(diagram):
            return True

        return bool(self.__get_user_access_by_diagram(diagram))

    def __get_user_access_by_diagram(self, diagram: Diagram) -> Optional[UserAccess]:
        return next((user_access for user_access in self.shared_diagrams if user_access.diagram == diagram), None)
