from typing import Optional

from c4maker_server.domain.entities.item_position import ItemPosition


class ItemPositionMapper:

    @staticmethod
    def entity_to_db(position: Optional[ItemPosition]) -> Optional[dict]:
        if not position:
            return None

        return {
            "x": position.x,
            "y": position.y,
            "width": position.width,
            "height": position.height
        }

    @staticmethod
    def db_to_entity(position_dto: Optional[dict]) -> Optional[ItemPosition]:
        if not position_dto:
            return None

        return ItemPosition(x=position_dto.get("x"), y=position_dto.get("y"), width=position_dto.get("width"),
                            height=position_dto.get("height"))
