class DomainException(Exception):
    """
    Base class for domain exceptions.
    """

    pass


class TodoNotFoundException(DomainException):
    """
    Exception raised when a todo is not found.
    """

    pass


class InvalidTodoStateError(DomainException):
    """
    Exception raised when a todo has an invalid state.
    """

    pass
