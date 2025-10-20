class DomainException(Exception):
    """Base domain exception"""

    pass


class TodoNotFoundError(DomainException):
    """Raised when a todo is not found"""

    pass


class InvalidTodoStateError(DomainException):
    """Raised when todo state transition is invalid"""

    pass
