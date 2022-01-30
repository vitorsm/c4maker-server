from uuid import UUID


class EntityNotFoundException(Exception):
    def __init__(self, entity_type: str, entity_id: UUID):
        super().__init__(f"The {entity_type} {entity_id} was not found")
