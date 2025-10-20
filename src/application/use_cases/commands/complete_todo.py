from dataclasses import dataclass

from domain.events.todo_events import TodoCompleted
from domain.exceptions import TodoNotFoundError
from domain.value_objects.todo_id import TodoId
from ...interfaces.event_bus import EventBus
from ...interfaces.unit_of_work import UnitOfWork


@dataclass
class CompleteTodoCommand:
    todo_id: str
    user_id: str


class CompleteTodoHandler:
    def __init__(self, uow: UnitOfWork, event_bus: EventBus):
        self.uow = uow
        self.event_bus = event_bus

    async def handle(self, command: CompleteTodoCommand) -> None:
        async with self.uow:
            todo = await self.uow.todos.find_by_id(TodoId(command.todo_id))
            if not todo:
                raise TodoNotFoundError(f"Todo {command.todo_id} not found")

            todo.complete()

            await self.uow.todos.save(todo)

            event = TodoCompleted(todo_id=todo.id, user_id=command.user_id)
            await self.event_bus.publish(event)

            await self.uow.commit()
