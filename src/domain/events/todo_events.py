from dataclasses import dataclass

from ..value_objects.todo_id import TodoId
from .base import DomainEvent


@dataclass
class TodoCreated(DomainEvent):
    todo_id: TodoId
    title: str
    user_id: str


@dataclass
class TodoCompleted(DomainEvent):
    todo_id: TodoId
    user_id: str


@dataclass
class TodoDeleted(DomainEvent):
    todo_id: TodoId
    user_id: str
