from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from domain.exceptions import DomainException
from .v1.schemas import ErrorResponse


async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            detail=str(exc), error_code=type(exc).__name__
        ).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    field_errors = [
        {"field": ".".join(map(str, error["loc"])), "message": error["msg"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            detail="Validation error", field_errors=field_errors
        ).dict(),
    )
