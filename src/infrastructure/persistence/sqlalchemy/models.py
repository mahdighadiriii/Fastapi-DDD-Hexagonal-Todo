import uuid

from sqlalchemy import JSON, Column, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, index=True)
    priority = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    tags = Column(JSON, default=list)
    user_id = Column(String(100), nullable=False, index=True)

    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
        Index("idx_user_priority", "user_id", "priority"),
        Index("idx_due_date", "due_date"),
    )
