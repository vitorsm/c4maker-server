import uuid
from datetime import datetime

from c4maker_server.domain.entities.diagram import Diagram, DiagramType
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship
from c4maker_server.domain.entities.user import User
from c4maker_server.domain.entities.user_access import UserAccess, UserPermission
from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.domain.entities.workspace_item import WorkspaceItem, WorkspaceItemType
from c4maker_server.utils import date_utils


class DefaultValues:
    """
    The integration test will be executed using an existing database.
    The data is loaded by the file c4maker-server/resources/initial_load.sql.
    These functions will return those data instance
    """

    DEFAULT_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")
    SECONDARY_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
    OTHER_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")
    NOT_PERSISTED_ID = uuid.UUID("00000000-0000-0000-0000-000000000099")

    @staticmethod
    def get_default_user() -> User:
        return User(id=DefaultValues.DEFAULT_ID, name="User 1", login="user",
                    password="$2b$12$eSoRK4Da8sEX3GSg56FKmujEq2JdeaMIt98nHKfdusf78UzzSaOCS",
                    user_access=list())

    @staticmethod
    def get_secondary_user() -> User:
        return User(id=DefaultValues.SECONDARY_ID, name="User 2", login="user2",
                    password="$2b$12$eSoRK4Da8sEX3GSg56FKmujEq2JdeaMIt98nHKfdusf78UzzSaOCS",
                    user_access=list())

    @staticmethod
    def get_default_date() -> datetime:
        return date_utils.str_iso_to_date("2022-01-01T07:44:42.000")

    @staticmethod
    def get_default_workspace() -> Workspace:
        return Workspace(id=DefaultValues.DEFAULT_ID, name="Workspace 1", description="Desc 1",
                         created_by=DefaultValues.get_default_user(), modified_by=DefaultValues.get_default_user(),
                         created_at=DefaultValues.get_default_date(), modified_at=DefaultValues.get_default_date())

    @staticmethod
    def get_default_diagram() -> Diagram:
        return Diagram(id=DefaultValues.DEFAULT_ID, name="Diagram 1", description="Desc 1",
                       workspace=DefaultValues.get_default_workspace(), diagram_type=DiagramType.C4,
                       created_by=DefaultValues.get_default_user(), modified_by=DefaultValues.get_default_user(),
                       created_at=DefaultValues.get_default_date(), modified_at=DefaultValues.get_default_date())

    @staticmethod
    def get_default_user_with_access() -> User:
        user = DefaultValues.get_default_user()
        workspace = DefaultValues.get_default_workspace()
        user.user_access = [UserAccess(workspace=workspace, permission=UserPermission.EDIT)]

        return user

    @staticmethod
    def get_default_workspace_item() -> WorkspaceItem:
        user = DefaultValues.get_default_user()

        return WorkspaceItem(id=DefaultValues.DEFAULT_ID, workspace=DefaultValues.get_default_workspace(),
                             workspace_item_type=WorkspaceItemType.PERSONA, key="item1", name="Item 1",
                             description="Desc 1", details="Details 1", created_by=user, modified_by=user,
                             created_at=DefaultValues.get_default_date(), modified_at=DefaultValues.get_default_date())

    @staticmethod
    def get_secondary_workspace_item() -> WorkspaceItem:
        user = DefaultValues.get_default_user()

        return WorkspaceItem(id=DefaultValues.SECONDARY_ID, workspace=DefaultValues.get_default_workspace(),
                             workspace_item_type=WorkspaceItemType.CONTAINER, key="item2", name="Item 2",
                             description="Desc 2", details="Details 2", created_by=user, modified_by=user,
                             created_at=DefaultValues.get_default_date(), modified_at=DefaultValues.get_default_date())

    @staticmethod
    def get_other_workspace_item() -> WorkspaceItem:
        user = DefaultValues.get_default_user()

        return WorkspaceItem(id=DefaultValues.OTHER_ID, workspace=DefaultValues.get_default_workspace(),
                             workspace_item_type=WorkspaceItemType.CONTAINER, key="item3", name="Item 3",
                             description="Desc 3", details="Details 3", created_by=user, modified_by=user,
                             created_at=DefaultValues.get_default_date(), modified_at=DefaultValues.get_default_date())

    @staticmethod
    def get_other_diagram_item() -> DiagramItem:
        return DiagramItem(id=DefaultValues.OTHER_ID, workspace_item=DefaultValues.get_other_workspace_item(),
                           diagram=DefaultValues.get_default_diagram())

    @staticmethod
    def get_default_diagram_item() -> DiagramItem:
        another_diagram_item = DefaultValues.get_other_diagram_item()
        relationship = [DiagramItemRelationship(diagram_item=another_diagram_item, description="uses",
                                                details="details")]
        return DiagramItem(id=DefaultValues.DEFAULT_ID, workspace_item=DefaultValues.get_default_workspace_item(),
                           diagram=DefaultValues.get_default_diagram(), relationships=relationship)
