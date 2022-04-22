

class DuplicateEntityException(Exception):
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f"The {entity_type} {entity_id} is already persisted")
