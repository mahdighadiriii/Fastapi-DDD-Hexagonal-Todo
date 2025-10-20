from datetime import datetime
from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PriorityEnum(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class TodoStatusEnum(str, BaseModel):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CreateTodoRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.MEDIUM
    due_date: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list, max_items=10)


class UpdateTodoRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = Field(None, max_items=10)


class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: TodoStatusEnum
    priority: PriorityEnum
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    due_date: Optional[datetime]
    tags: List[str]
    is_overdue: bool

    model_config = ConfigDict(from_attributes=True)


class TodoListResponse(BaseModel):
    items: List[TodoResponse]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    field_errors: Optional[List[dict]] = None
