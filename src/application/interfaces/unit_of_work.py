from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.domain.repositories.todo_repository import TodoRepository

T = TypeVar("T")


class UnitOfWork(ABC, Generic[T]):
    todos: TodoRepository

    @abstractmethod
    async def __aenter__(self) -> T:
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
