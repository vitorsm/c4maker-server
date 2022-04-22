from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime

from c4maker_server.adapters.models.base_model import BaseModel


class DiagramDB(BaseModel):
    __tablename__ = "diagram"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    created_by = Column(String, ForeignKey("user.id"), nullable=False)
    modified_by = Column(String, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
