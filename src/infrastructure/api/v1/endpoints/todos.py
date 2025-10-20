from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.application.use_cases.commands.complete_todo import CompleteTodoCommand
from src.domain.value_objects.priority import Priority
from src.domain.value_objects.todo_status import TodoStatus

from src.application.use_cases.commands.create_todo import CreateTodoCommand
from src.application.use_cases.queries.list_todos import (
    ListTodosQuery,
    SortField,
    SortOrder,
)
from src.domain.exceptions import InvalidTodoStateError, TodoNotFoundError

from ..dependencies import (
    get_complete_todo_handler,
    get_create_todo_handler,
    get_current_user,
    get_get_todo_handler,
    get_list_todos_handler,
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

    # Get created todo
    get_handler = await get_get_todo_handler()
    todo = await get_handler.handle(todo_id, current_user["id"])

    return TodoResponse(**todo.dict())


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
        items=[TodoResponse(**todo.dict()) for todo in todos],
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
        return TodoResponse(**todo.dict())
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

        # Get updated todo
        get_handler = await get_get_todo_handler()
        todo = await get_handler.handle(todo_id, current_user["id"])

        return TodoResponse(**todo.dict())
    except TodoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo {todo_id} not found"
        )
    except InvalidTodoStateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
