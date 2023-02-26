from typing import Optional

from c4maker_server.application.api.mapper.generic_mapper import GenericMapper
from c4maker_server.application.api.mapper.reduced_workspace_mapper import ReducedWorkspaceMapper
from c4maker_server.domain.entities.workspace_item import WorkspaceItem
from c4maker_server.utils import utils


class WorkspaceItemMapper:

    @staticmethod
    def to_entity(dto: dict) -> Optional[WorkspaceItem]:
        if not dto:
            return None

        return WorkspaceItem(id=utils.str_to_uuid(dto.get("id")),
                             workspace=ReducedWorkspaceMapper.to_entity(dto.get("workspace")),
                             workspace_item_type=WorkspaceItem.instantiate_item_type_by_name(dto.get("item_type")),
                             key=dto.get("key"), name=dto.get("name"), description=dto.get("description"),
                             details=dto.get("details"))

    @staticmethod
    def to_dto(workspace_item: WorkspaceItem) -> Optional[dict]:
        if not workspace_item:
            return None

        dto = {
            "id": str(workspace_item.id),
            "workspace": ReducedWorkspaceMapper.to_dto(workspace_item.workspace),
            "item_type": workspace_item.workspace_item_type.name,
            "key": workspace_item.key,
            "name": workspace_item.name,
            "description": workspace_item.description,
            "details": workspace_item.details
        }

        GenericMapper.to_dto(workspace_item, dto)

        return dto
