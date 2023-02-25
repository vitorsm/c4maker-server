from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from c4maker_server.domain.entities.user_access import UserAccess, UserPermission
from c4maker_server.domain.entities.workspace import Workspace


@dataclass
class User:
    id: UUID
    name: str
    login: str
    password: str
    user_access: List[UserAccess]

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

    def is_owner(self, workspace: Workspace) -> bool:
        return workspace.created_by == self

    def allowed_to_edit(self, workspace: Workspace) -> bool:
        if self.is_owner(workspace):
            return True

        user_access = self.__get_user_access_by_diagram(workspace)

        if not user_access:
            return False

        return user_access.permission == UserPermission.EDIT

    def allowed_to_view(self, workspace: Workspace) -> bool:
        if self.is_owner(workspace):
            return True

        return bool(self.__get_user_access_by_diagram(workspace))

    def __get_user_access_by_diagram(self, workspace: Workspace) -> Optional[UserAccess]:
        return next((user_access for user_access in self.user_access if user_access.workspace == workspace), None)
