from typing import Optional
from uuid import UUID


def str_to_uuid(str_uuid: str) -> Optional[UUID]:
    if not str_uuid:
        return None

    return UUID(str_uuid)
