from typing import List, Optional
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy

from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.services.ports.diagram_item_repository import DiagramItemRepository


class MySQLDiagramItemRepository(DiagramItemRepository):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, diagram_item: DiagramItem):
        pass

    def update(self, diagram_item: DiagramItem):
        pass

    def delete(self, diagram_item_id: UUID):
        pass

    def find_by_id(self, diagram_item_id: UUID) -> Optional[DiagramItem]:
        pass

    def find_all_by_diagram(self, diagram_id: UUID) -> List[DiagramItem]:
        pass
