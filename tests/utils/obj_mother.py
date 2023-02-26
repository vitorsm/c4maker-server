import uuid
import random
import string
from enum import Enum
from typing import Optional, List, Type

from c4maker_server.domain.entities.diagram import DiagramType, Diagram
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.user_access import UserAccess
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.domain.entities.workspace_item import WorkspaceItemType, WorkspaceItem


class ObjMother:

    @staticmethod
    def generate_random_str(length: int) -> str:
        return ''.join([random.choice(string.ascii_letters) for i in range(length)])

    @staticmethod
    def get_random_enum_value(enum_type: Type[Enum]) -> Enum:
        types = list(map(lambda t: t, enum_type))
        return random.choice(types)

    @staticmethod
    def generate_random_user(user_id: Optional[uuid.UUID] = None, name: Optional[str] = None,
                             login: Optional[str] = None, password: Optional[str] = None,
                             user_access: Optional[List[UserAccess]] = None):
        if not user_id:
            user_id = uuid.uuid4()

        if name is None:
            name = ObjMother.generate_random_str(10)
        if login is None:
            login = ObjMother.generate_random_str(15)
        if password is None:
            password = ObjMother.generate_random_str(15)

        return User(id=user_id, name=name, login=login, password=password, user_access=user_access)

    @staticmethod
    def generate_random_workspace(workspace_id: Optional[uuid.UUID] = None, name: Optional[str] = None,
                                  description: Optional[str] = None, user: Optional[User] = None) -> Workspace:
        if workspace_id is None:
            workspace_id = uuid.uuid4()
        if name is None:
            name = ObjMother.generate_random_str(10)
        if description is None:
            description = ObjMother.generate_random_str(100)

        return Workspace(id=workspace_id, name=name, description=description, created_by=user, modified_by=user)

    @staticmethod
    def generate_random_diagram(diagram_id: Optional[uuid.UUID] = None, name: Optional[str] = None,
                                description: Optional[str] = None, workspace: Optional[Workspace] = None,
                                diagram_type: Optional[DiagramType] = None):
        if not diagram_id:
            diagram_id = uuid.uuid4()
        if name is None:
            name = ObjMother.generate_random_str(10)
        if description is None:
            description = ObjMother.generate_random_str(100)
        if not workspace:
            workspace = ObjMother.generate_random_workspace()
        if not diagram_type:
            diagram_type = ObjMother.get_random_enum_value(DiagramType)

        return Diagram(id=diagram_id, name=name, description=description, workspace=workspace,
                       diagram_type=diagram_type)

    @staticmethod
    def generate_random_workspace_item(w_id: Optional[uuid.UUID] = None, key: Optional[str] = None,
                                       name: Optional[str] = None, description: Optional[str] = None,
                                       details: Optional[str] = None, workspace: Optional[Workspace] = None,
                                       w_type: Optional[WorkspaceItemType] = None, user: Optional[User] = None) -> WorkspaceItem:
        if not w_id:
            w_id = uuid.uuid4()
        if name is None:
            name = ObjMother.generate_random_str(10)
        if key is None:
            key = ObjMother.generate_random_str(15)
        if description is None:
            description = ObjMother.generate_random_str(100)
        if details is None:
            details = ObjMother.generate_random_str(100)
        if workspace is None:
            workspace = ObjMother.generate_random_workspace()
        if not w_type:
            w_type = ObjMother.get_random_enum_value(WorkspaceItemType)

        return WorkspaceItem(id=w_id, name=name, description=description, details=details, workspace=workspace,
                             workspace_item_type=w_type, key=key, created_by=user, modified_by=user)
