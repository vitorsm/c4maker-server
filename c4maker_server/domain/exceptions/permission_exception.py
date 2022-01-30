from uuid import UUID

from c4maker_server.domain.entities.user import User


class PermissionException(Exception):
    def __init__(self, entity_type: str, entity_id: UUID, user: User):
        super().__init__(f"The user {user.login} has no permission to manage {entity_type} {entity_id}")
