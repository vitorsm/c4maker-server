import abc
from typing import Optional, List
from uuid import UUID

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item import DiagramItem


class DiagramItemRepository(metaclass=abc.ABCMeta):

    def create(self, diagram_item: DiagramItem):
        raise NotImplementedError

    def update(self, diagram_item: DiagramItem):
        raise NotImplementedError

    def delete(self, diagram_item_id: UUID):
        raise NotImplementedError

    def find_by_id(self, diagram_item_id: UUID) -> Optional[DiagramItem]:
        raise NotImplementedError

    def find_all_by_diagram(self, diagram: Diagram) -> List[DiagramItem]:
        raise NotImplementedError
