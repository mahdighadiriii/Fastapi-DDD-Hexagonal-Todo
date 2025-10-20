from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ..exceptions import InvalidTodoStateError
from ..value_objects.priority import Priority
from ..value_objects.todo_id import TodoId
from ..value_objects.todo_status import TodoStatus


@dataclass
class Todo:
    id: TodoId
    title: str
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.PENDING
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)

    def complete(self) -> None:
        if self.status == TodoStatus.COMPLETED:
            raise InvalidTodoStateError("Todo is already completed")
        self.status = TodoStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def is_overdue(self) -> bool:
        if self.due_date is None or self.status == TodoStatus.COMPLETED:
            return False
        return self.due_date < datetime.datetime()
