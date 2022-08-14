from typing import Any

from c4maker_server.application.api.mapper.reduced_user_mapper import ReducedUserMapper
from c4maker_server.utils import date_utils


class GenericMapper:

    @staticmethod
    def to_dto(entity: Any, dto: dict):
        if hasattr(entity, "created_by"):
            dto["created_by"] = ReducedUserMapper.to_dto(entity.created_by)
        if hasattr(entity, "modified_by"):
            dto["modified_by"] = ReducedUserMapper.to_dto(entity.modified_by)
        if hasattr(entity, "created_at"):
            dto["created_at"] = date_utils.datetime_to_str(entity.created_at)
        if hasattr(entity, "modified_at"):
            dto["modified_at"] = date_utils.datetime_to_str(entity.modified_at)
