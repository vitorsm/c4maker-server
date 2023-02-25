from typing import List


class InvalidEntityException(Exception):
    missing_fields: List[str]

    def __init__(self, entity_type: str, missing_fields: List[str]):
        super().__init__(f"The {entity_type} is invalid. The following fields is missing: {', '.join(missing_fields)}")
        self.missing_fields = missing_fields
