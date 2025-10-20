from dataclasses import dataclass

from .base import DomainEvent
from ..value_objects.todo_id import TodoId


@dataclass(kw_only=True)
class TodoCreated(DomainEvent):
    todo_id: TodoId
    title: str
    user_id: str


@dataclass(kw_only=True)
class TodoCompleted(DomainEvent):
    todo_id: TodoId
    user_id: str


@dataclass(kw_only=True)
class TodoDeleted(DomainEvent):
    todo_id: TodoId
    user_id: str
