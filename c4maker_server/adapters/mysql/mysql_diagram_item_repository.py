from typing import List, Optional
from uuid import UUID

from c4maker_server.adapters.models import DiagramItemDB
from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.domain.entities.diagram import Diagram
from c4maker_server.domain.entities.diagram_item import DiagramItem
from c4maker_server.services.ports.diagram_item_repository import DiagramItemRepository


class MySQLDiagramItemRepository(DiagramItemRepository):
    def __init__(self, mysql_client: MySQLClient):
        self.mysql_client = mysql_client

    def create(self, diagram_item: DiagramItem):
        diagram_item_db = DiagramItemDB(diagram_item)
        self.mysql_client.add(diagram_item_db)

    def update(self, diagram_item: DiagramItem):
        diagram_item_db = self.__find_db_obj_by_id(str(diagram_item.id))
        diagram_item_db.update_properties(diagram_item)
        self.mysql_client.update(diagram_item_db)

    def delete(self, diagram_item_id: UUID):
        diagram_item_db = self.__find_db_obj_by_id(str(diagram_item_id))
        self.mysql_client.delete(diagram_item_db)

    def find_by_id(self, diagram_item_id: UUID) -> Optional[DiagramItem]:
        diagram_item_db = self.__find_db_obj_by_id(str(diagram_item_id))

        if not diagram_item_db:
            return None

        return diagram_item_db.to_entity(None)

    def find_all_by_diagram(self, diagram: Diagram) -> List[DiagramItem]:
        diagram_items_db = self.mysql_client.db.session.query(DiagramItemDB) \
            .filter(DiagramItemDB.diagram_id == str(diagram.id))

        return [d.to_entity(diagram) for d in diagram_items_db]

    def __find_db_obj_by_id(self, diagram_item_id: str) -> DiagramItemDB:
        return self.mysql_client.db.session.query(DiagramItemDB).get(diagram_item_id)
