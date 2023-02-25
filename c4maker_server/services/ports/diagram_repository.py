import abc
from typing import Optional, List
from uuid import UUID

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.user import User


class DiagramRepository(metaclass=abc.ABCMeta):

    def create(self, diagram: Diagram):
        raise NotImplementedError

    def update(self, diagram: Diagram):
        raise NotImplementedError

    def delete(self, diagram_id: UUID):
        raise NotImplementedError

    def find_by_id(self, diagram_id: UUID) -> Optional[Diagram]:
        raise NotImplementedError

    def find_by_workspace_id(self, workspace_id: UUID) -> List[Diagram]:
        raise NotImplementedError
