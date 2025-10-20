from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository
from domain.value_objects.priority import Priority
from domain.value_objects.todo_id import TodoId
from domain.value_objects.todo_status import TodoStatus

from .models import TodoModel


class SQLAlchemyTodoRepository(TodoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, todo: Todo) -> None:
        model = await self.session.get(TodoModel, str(todo.id))

        if model is None:
            model = TodoModel()

        model.id = str(todo.id)
        model.title = todo.title
        model.description = todo.description
        model.status = todo.status.value
        model.priority = todo.priority.value
        model.created_at = todo.created_at
        model.updated_at = todo.updated_at
        model.completed_at = todo.completed_at
        model.due_date = todo.due_date
        model.tags = todo.tags

        self.session.add(model)
        await self.session.flush()

    async def find_by_id(self, todo_id: TodoId) -> Optional[Todo]:
        model = await self.session.get(TodoModel, str(todo_id))
        return self._to_entity(model) if model else None

    async def find_all(self) -> List[Todo]:
        result = await self.session.execute(select(TodoModel))
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def find_by_status(self, status: TodoStatus) -> List[Todo]:
        result = await self.session.execute(
            select(TodoModel).where(TodoModel.status == status.value)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def delete(self, todo_id: TodoId) -> None:
        model = await self.session.get(TodoModel, str(todo_id))
        if model:
            await self.session.delete(model)
            await self.session.flush()

    async def exists(self, todo_id: TodoId) -> bool:
        result = await self.session.execute(
            select(func.count())
            .select_from(TodoModel)
            .where(TodoModel.id == str(todo_id))
        )
        return result.scalar() > 0

    def _to_entity(self, model: TodoModel) -> Todo:
        return Todo(
            id=TodoId(str(model.id)),
            title=model.title,
            description=model.description,
            status=TodoStatus(model.status),
            priority=Priority(model.priority),
            created_at=model.created_at,
            updated_at=model.updated_at,
            completed_at=model.completed_at,
            due_date=model.due_date,
            tags=model.tags,
        )
