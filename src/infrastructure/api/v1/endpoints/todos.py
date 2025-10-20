from typing import Annotated, List, Optional

from ....events.event_bus import InMemoryEventBus
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ....persistence.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork

from application.use_cases.commands.complete_todo import (
    CompleteTodoCommand,
    CompleteTodoHandler,
)
from application.use_cases.commands.create_todo import (
    CreateTodoCommand,
    CreateTodoHandler,
)
from application.use_cases.commands.update_todo import (
    UpdateTodoCommand,
    UpdateTodoHandler,
)
from application.use_cases.queries.get_todo import GetTodoHandler
from application.use_cases.queries.list_todos import (
    ListTodosHandler,
    ListTodosQuery,
    SortField,
    SortOrder,
)
from domain.exceptions import InvalidTodoStateError, TodoNotFoundError
from domain.value_objects.priority import Priority
from domain.value_objects.todo_status import TodoStatus

from ..dependencies import (
    get_complete_todo_handler,
    get_create_todo_handler,
    get_current_user,
    get_event_bus,
    get_get_todo_handler,
    get_list_todos_handler,
    get_unit_of_work,
)
from ..schemas import (
    CreateTodoRequest,
    TodoListResponse,
    TodoResponse,
    TodoStatusEnum,
    UpdateTodoRequest,
)

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    request: CreateTodoRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
    handler: Annotated[CreateTodoHandler, Depends(get_create_todo_handler)],
):
    """Create a new todo"""
    command = CreateTodoCommand(
        title=request.title,
        description=request.description,
        priority=Priority(request.priority),
        due_date=request.due_date,
        tags=request.tags,
        user_id=current_user["id"],
    )

    todo_id = await handler.handle(command)

    get_handler = get_get_todo_handler()
    todo = await get_handler.handle(todo_id, current_user["id"])

    return TodoResponse(**todo.__dict__)


@router.get("/", response_model=TodoListResponse)
async def list_todos(
    current_user: Annotated[dict, Depends(get_current_user)],
    handler: Annotated[ListTodosHandler, Depends(get_list_todos_handler)],
    status: Optional[TodoStatusEnum] = None,
    priority: Optional[int] = Query(None, ge=1, le=4),
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = None,
    sort_by: SortField = SortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List todos with filtering and pagination"""
    query = ListTodosQuery(
        user_id=current_user["id"],
        status=TodoStatus(status) if status else None,
        priority=Priority(priority) if priority else None,
        tags=tags,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )

    todos, total = await handler.handle(query)

    return TodoListResponse(
        items=[TodoResponse(**todo.__dict__) for todo in todos],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    handler: Annotated[GetTodoHandler, Depends(get_get_todo_handler)],
):
    """Get a specific todo"""
    try:
        todo = await handler.handle(todo_id, current_user["id"])
        return TodoResponse(**todo.__dict__)
    except TodoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo {todo_id} not found"
        )


@router.post("/{todo_id}/complete", response_model=TodoResponse)
async def complete_todo(
    todo_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    handler: Annotated[CompleteTodoHandler, Depends(get_complete_todo_handler)],
):
    """Complete a todo"""
    try:
        command = CompleteTodoCommand(todo_id=todo_id, user_id=current_user["id"])

        await handler.handle(command)

        get_handler = get_get_todo_handler()
        todo = await get_handler.handle(todo_id, current_user["id"])

        return TodoResponse(**todo.__dict__)
    except TodoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo {todo_id} not found"
        )
    except InvalidTodoStateError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    request: UpdateTodoRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_unit_of_work)],
    event_bus: Annotated[InMemoryEventBus, Depends(get_event_bus)],
):
    """Update a todo"""
    handler = UpdateTodoHandler(uow, event_bus)
    command = UpdateTodoCommand(
        todo_id=todo_id,
        title=request.title,
        description=request.description,
        priority=Priority(request.priority) if request.priority else None,
        due_date=request.due_date,
        tags=request.tags,
        user_id=current_user["id"],
    )

    try:
        await handler.handle(command)

        get_handler = get_get_todo_handler()
        todo = await get_handler.handle(todo_id, current_user["id"])

        return TodoResponse(**todo.__dict__)
    except TodoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo {todo_id} not found"
        )
