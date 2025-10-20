from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.exceptions import TodoNotFoundError
from domain.value_objects.priority import Priority
from domain.value_objects.todo_id import TodoId
from ...interfaces.event_bus import EventBus
from ...interfaces.unit_of_work import UnitOfWork


@dataclass
class UpdateTodoCommand:
    todo_id: str
    title: Optional[str]
    description: Optional[str]
    priority: Optional[Priority]
    due_date: Optional[datetime]
    tags: Optional[list[str]]
    user_id: str


class UpdateTodoHandler:
    def __init__(self, uow: UnitOfWork, event_bus: EventBus):
        self.uow = uow
        self.event_bus = event_bus

    async def handle(self, command: UpdateTodoCommand) -> None:
        async with self.uow:
            todo = await self.uow.todos.find_by_id(TodoId(command.todo_id))
            if not todo:
                raise TodoNotFoundError(f"Todo {command.todo_id} not found")

            if command.title is not None:
                todo.title = command.title
            if command.description is not None:
                todo.description = command.description
            if command.priority is not None:
                todo.priority = command.priority
            if command.due_date is not None:
                todo.due_date = command.due_date
            if command.tags is not None:
                todo.tags = command.tags

            todo.updated_at = datetime.utcnow()

            await self.uow.todos.save(todo)
            await self.uow.commit()
