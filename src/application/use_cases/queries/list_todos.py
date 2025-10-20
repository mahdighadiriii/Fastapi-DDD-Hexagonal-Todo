from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

from domain.value_objects.todo_status import TodoStatus
from domain.value_objects.priority import Priority
from ...dto.todo_dto import TodoDTO


class SortField(Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    DUE_DATE = "due_date"
    PRIORITY = "priority"


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class ListTodosQuery:
    user_id: str
    status: Optional[TodoStatus] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None
    sort_by: SortField = SortField.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC
    limit: int = 20
    offset: int = 0


class ListTodosHandler:
    def __init__(self, todo_read_repository):
        self.todo_read_repository = todo_read_repository
    
    async def handle(self, query: ListTodosQuery) -> tuple[List[TodoDTO], int]:
        todos, total = await self.todo_read_repository.find_with_filters(
            user_id=query.user_id,
            status=query.status,
            priority=query.priority,
            tags=query.tags,
            search=query.search,
            sort_by=query.sort_by.value,
            sort_order=query.sort_order.value,
            limit=query.limit,
            offset=query.offset
        )
        
        return [self._to_dto(todo) for todo in todos], total
    
    def _to_dto(self, todo) -> TodoDTO:
        return TodoDTO(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            status=todo.status.value,
            priority=todo.priority.value,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            completed_at=todo.completed_at,
            due_date=todo.due_date,
            tags=todo.tags,
            is_overdue=todo.is_overdue()
        )