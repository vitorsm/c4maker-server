from typing import List, Optional
from uuid import UUID

from c4maker_server.adapters.models import DiagramDB
from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.services.ports.diagram_repository import DiagramRepository


class MySQLDiagramRepository(DiagramRepository):

    def __init__(self, mysql_client: MySQLClient):
        self.mysql_client = mysql_client

    def create(self, diagram: Diagram):
        diagram_db = DiagramDB(diagram)
        self.mysql_client.add(diagram_db)

    def update(self, diagram: Diagram):
        diagram_db = self.__find_db_obj_by_id(str(diagram.id))
        diagram_db.update_properties(diagram)
        self.mysql_client.update(diagram_db)

    def delete(self, diagram_id: UUID):
        diagram_db = self.__find_db_obj_by_id(str(diagram_id))

        if not diagram_db:
            return

        self.mysql_client.delete(diagram_db)

    def find_by_id(self, diagram_id: UUID) -> Optional[Diagram]:
        diagram_db = self.__find_db_obj_by_id(str(diagram_id))

        if not diagram_db:
            return None

        return diagram_db.to_entity()

    def find_by_workspace_id(self, workspace_id: UUID) -> List[Diagram]:
        diagrams_db = self.mysql_client.db.session.query(DiagramDB).filter(DiagramDB.workspace_id == str(workspace_id))
        return [diagram_db.to_entity() for diagram_db in diagrams_db]

    def __find_db_obj_by_id(self, diagram_id: str) -> DiagramDB:
        return self.mysql_client.db.session.query(DiagramDB).get(diagram_id)
