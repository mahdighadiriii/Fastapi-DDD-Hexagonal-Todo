from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.application.use_cases.commands.complete_todo import CompleteTodoHandler
from src.application.use_cases.queries.get_todo import GetTodoHandler
from src.infrastructure.events.event_bus import InMemoryEventBus

from src.application.use_cases.commands.create_todo import CreateTodoHandler
from src.application.use_cases.queries.list_todos import ListTodosHandler
from src.infrastructure.persistence.sqlalchemy.database import get_session
from src.infrastructure.persistence.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    # In real app, validate JWT token and return user
    # For demo, return dummy user
    return {"id": "user123", "email": "user@example.com"}


async def get_unit_of_work(session: Annotated[AsyncSession, Depends(get_session)]):
    return SQLAlchemyUnitOfWork(session)


def get_event_bus():
    return InMemoryEventBus()


async def get_create_todo_handler(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)],
    event_bus: Annotated[InMemoryEventBus, Depends(get_event_bus)],
) -> CreateTodoHandler:
    return CreateTodoHandler(uow, event_bus)


async def get_complete_todo_handler(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)],
    event_bus: Annotated[InMemoryEventBus, Depends(get_event_bus)],
) -> CompleteTodoHandler:
    return CompleteTodoHandler(uow, event_bus)


async def get_list_todos_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ListTodosHandler:
    from src.infrastructure.persistence.sqlalchemy.read_repositories import (
        TodoReadRepository,
    )

    read_repo = TodoReadRepository(session)
    return ListTodosHandler(read_repo)


async def get_get_todo_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> GetTodoHandler:
    from src.infrastructure.persistence.sqlalchemy.read_repositories import (
        TodoReadRepository,
    )

    read_repo = TodoReadRepository(session)
    return GetTodoHandler(read_repo)
