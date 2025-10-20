from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.commands.complete_todo import CompleteTodoHandler
from application.use_cases.commands.create_todo import CreateTodoHandler
from application.use_cases.commands.update_todo import UpdateTodoHandler
from application.use_cases.queries.get_todo import GetTodoHandler
from application.use_cases.queries.list_todos import ListTodosHandler

from ...events.event_bus import InMemoryEventBus
from ...persistence.sqlalchemy.database import get_session
from ...persistence.sqlalchemy.read_repositories import TodoReadRepository
from ...persistence.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    return {"id": "user123", "email": "user@example.com"}


async def get_unit_of_work(session: Annotated[AsyncSession, Depends(get_session)]):
    return SQLAlchemyUnitOfWork(session)


def get_event_bus():
    return InMemoryEventBus()


def get_create_todo_handler(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)],
    event_bus: Annotated[InMemoryEventBus, Depends(get_event_bus)],
) -> CreateTodoHandler:
    return CreateTodoHandler(uow, event_bus)


def get_complete_todo_handler(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)],
    event_bus: Annotated[InMemoryEventBus, Depends(get_event_bus)],
) -> CompleteTodoHandler:
    return CompleteTodoHandler(uow, event_bus)


def get_update_todo_handler(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)],
    event_bus: Annotated[InMemoryEventBus, Depends(get_event_bus)],
) -> UpdateTodoHandler:
    return UpdateTodoHandler(uow, event_bus)


# Query Handlers
def get_list_todos_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ListTodosHandler:
    read_repo = TodoReadRepository(session)
    return ListTodosHandler(read_repo)


def get_get_todo_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> GetTodoHandler:
    read_repo = TodoReadRepository(session)
    return GetTodoHandler(read_repo)
