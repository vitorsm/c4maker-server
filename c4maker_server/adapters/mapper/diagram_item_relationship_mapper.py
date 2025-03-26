
from c4maker_server.adapters.mapper.item_position_mapper import ItemPositionMapper
from c4maker_server.domain.entities.c4_diagram_item_relationship import C4DiagramItemRelationship
from c4maker_server.domain.entities.diagram import DiagramType
from c4maker_server.domain.entities.diagram_item_relationship import DiagramItemRelationship


class DiagramItemRelationshipMapper:

    @staticmethod
    def db_to_entity(diagram_item_relationship: DiagramItemRelationship, data: dict,
                     diagram_type: int) -> DiagramItemRelationship:
        if diagram_type == DiagramType.C4.value:
            return DiagramItemRelationshipMapper.__db_to_c4_entity(diagram_item_relationship, data)

        raise ValueError("Invalid diagram type %s", diagram_type)

    @staticmethod
    def entity_to_db(diagram_item_relationship: DiagramItemRelationship) -> dict:
        if isinstance(diagram_item_relationship, C4DiagramItemRelationship):
            return DiagramItemRelationshipMapper.__c4_entity_to_db(diagram_item_relationship)

        raise ValueError("Invalid diagram type %s", type(diagram_item_relationship))

    @staticmethod
    def __c4_entity_to_db(relationship: C4DiagramItemRelationship) -> dict:
        return {
            "from_position": ItemPositionMapper.entity_to_db(relationship.from_position),
            "to_position": ItemPositionMapper.entity_to_db(relationship.to_position)
        }

    @staticmethod
    def __db_to_c4_entity(relationship: DiagramItemRelationship, data: dict) -> C4DiagramItemRelationship:
        c4_relationship = C4DiagramItemRelationship(diagram_item=relationship.diagram_item,
                                                    description=relationship.description,
                                                    details=relationship.details)

        c4_relationship.to_position = ItemPositionMapper.db_to_entity(data.get("to_position"))
        c4_relationship.from_position = ItemPositionMapper.db_to_entity(data.get("from_position"))

        return c4_relationship
