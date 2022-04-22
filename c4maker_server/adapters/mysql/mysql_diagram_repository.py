from typing import List, Optional
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy

from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.user import User
from c4maker_server.services.ports.diagram_repository import DiagramRepository


class MySQLDiagramRepository(DiagramRepository):

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, diagram: Diagram):
        pass

    def update(self, diagram: Diagram):
        pass

    def delete(self, diagram_id: UUID):
        pass

    def find_by_id(self, diagram_id: UUID) -> Optional[Diagram]:
        pass

    def find_all_by_user(self, user: User) -> List[Diagram]:
        pass
