from typing import Optional

from c4maker_server.domain.entities.workspace import Workspace
from c4maker_server.utils import utils


class ReducedWorkspaceMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[Workspace]:
        if not dto:
            return None

        return Workspace(id=utils.str_to_uuid(dto.get("id")), name=dto.get("name"), description=dto.get("description"))

    @staticmethod
    def to_dto(workspace: Workspace) -> Optional[dict]:
        if not workspace:
            return None

        return {
            "id": str(workspace.id),
            "name": workspace.name,
            "description": workspace.description
        }
