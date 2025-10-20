from typing import List, Optional, Tuple

from sqlalchemy import and_, func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import literal

from domain.entities.todo import Todo
from domain.value_objects.priority import Priority
from domain.value_objects.todo_id import TodoId
from domain.value_objects.todo_status import TodoStatus

from .models import TodoModel
from .repositories import SQLAlchemyTodoRepository


class TodoReadRepository(SQLAlchemyTodoRepository):
    async def find_by_id(self, todo_id: TodoId, user_id: str) -> Optional[Todo]:
        result = await self.session.execute(
            select(TodoModel).where(
                and_(TodoModel.id == str(todo_id), TodoModel.user_id == user_id)
            )
        )
        model = result.scalar()
        return self._to_entity(model) if model else None

    async def find_with_filters(
        self,
        user_id: str,
        status: Optional[TodoStatus],
        priority: Optional[Priority],
        tags: Optional[List[str]],
        search: Optional[str],
        sort_by: str,
        sort_order: str,
        limit: int,
        offset: int,
    ) -> Tuple[List[Todo], int]:
        base_query = select(TodoModel).where(TodoModel.user_id == user_id)

        if status:
            base_query = base_query.where(TodoModel.status == status.value)
        if priority:
            base_query = base_query.where(TodoModel.priority == priority.value)
        if tags:
            base_query = base_query.where(TodoModel.tags.overlap(literal(tags)))
        if search:
            search_term = f"%{search}%"
            base_query = base_query.where(
                or_(
                    TodoModel.title.ilike(search_term),
                    TodoModel.description.ilike(search_term),
                )
            )

        count_query = select(func.count()).select_from(base_query.subquery())
        total = (await self.session.execute(count_query)).scalar()

        order_clause = text(f"{sort_by} {sort_order}")
        result = await self.session.execute(
            base_query.order_by(order_clause).limit(limit).offset(offset)
        )
        models = result.scalars().all()

        return [self._to_entity(model) for model in models], total
