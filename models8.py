from datetime import datetime
from enum import Enum as PyEnum
import uuid

from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import CHAR, TypeDecorator

from database import Base


class TaskStatus(PyEnum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return str(value)
        return str(value) if isinstance(value, uuid.UUID) else str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return value if isinstance(value, uuid.UUID) else uuid.UUID(value)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    schedule_for = Column(DateTime, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)