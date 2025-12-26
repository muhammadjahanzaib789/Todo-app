"""Domain-specific exceptions."""


class TaskNotFoundError(Exception):
    """Raised when a task with the given ID does not exist."""

    pass


class EmptyDescriptionError(Exception):
    """Raised when a task description is empty or whitespace-only."""

    pass
