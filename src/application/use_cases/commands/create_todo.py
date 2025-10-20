from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entities.todo import Todo
from domain.events.todo_events import TodoCreated
from domain.value_objects.priority import Priority
from domain.value_objects.todo_id import TodoId
from domain.value_objects.todo_status import TodoStatus
from ...interfaces.event_bus import EventBus
from ...interfaces.unit_of_work import UnitOfWork


@dataclass
class CreateTodoCommand:
    title: str
    description: Optional[str]
    priority: Priority
    due_date: Optional[datetime]
    tags: list[str]
    user_id: str


class CreateTodoHandler:
    def __init__(self, uow: UnitOfWork, event_bus: EventBus):
        self.uow = uow
        self.event_bus = event_bus

    async def handle(self, command: CreateTodoCommand) -> str:
        async with self.uow:
            todo = Todo(
                id=TodoId.generate(),
                title=command.title,
                description=command.description,
                status=TodoStatus.PENDING,
                priority=command.priority,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                due_date=command.due_date,
                tags=command.tags,
            )

            await self.uow.todos.save(todo)

            event = TodoCreated(
                todo_id=todo.id, title=todo.title, user_id=command.user_id
            )
            await self.event_bus.publish(event)

            await self.uow.commit()

            return str(todo.id)
