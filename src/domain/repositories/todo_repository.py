from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.todo import Todo
from ..value_objects.todo_id import TodoId
from ..value_objects.todo_status import TodoStatus


class TodoRepository(ABC):
    @abstractmethod
    async def save(self, todo: Todo) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, todo_id: TodoId) -> Optional[Todo]:
        pass

    @abstractmethod
    async def find_all(self) -> List[Todo]:
        pass

    @abstractmethod
    async def find_by_status(self, status: TodoStatus) -> List[Todo]:
        pass

    @abstractmethod
    async def delete(self, todo_id: TodoId) -> None:
        pass

    @abstractmethod
    async def exists(self, todo_id: TodoId) -> bool:
        pass