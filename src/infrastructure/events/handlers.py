from domain.events.todo_events import TodoCompleted, TodoCreated
from ..api.v1.dependencies import get_event_bus


async def handle_todo_created(event: TodoCreated):
    """Send notification when todo is created"""
    print(f"Todo {event.todo_id} created by {event.user_id}")


async def handle_todo_completed(event: TodoCompleted):
    """Update statistics when todo is completed"""
    print(f"Todo {event.todo_id} completed by {event.user_id}")


def register_event_handlers():
    event_bus = get_event_bus()
    event_bus.subscribe(TodoCreated, handle_todo_created)
    event_bus.subscribe(TodoCompleted, handle_todo_completed)
