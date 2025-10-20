from typing import Optional

from domain.exceptions import TodoNotFoundError
from domain.value_objects.todo_id import TodoId
from ...dto.todo_dto import TodoDTO


class GetTodoHandler:
    def __init__(self, todo_read_repository):
        self.todo_read_repository = todo_read_repository

    async def handle(self, todo_id: str, user_id: str) -> TodoDTO:
        todo = await self.todo_read_repository.find_by_id(TodoId(todo_id), user_id)
        if not todo:
            raise TodoNotFoundError(f"Todo {todo_id} not found")
        return self._to_dto(todo)

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
            is_overdue=todo.is_overdue(),
        )
