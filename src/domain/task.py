"""Task entity - core domain model."""

from dataclasses import dataclass
from src.domain.exceptions import EmptyDescriptionError


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique integer identifier (auto-generated, immutable)
        description: Text description of what needs to be done (required, non-empty)
        is_complete: Completion status (defaults to False)
    """

    id: int
    description: str
    is_complete: bool = False

    def __post_init__(self) -> None:
        """Validate task attributes after initialization."""
        if not self.description or not self.description.strip():
            raise EmptyDescriptionError("Task description cannot be empty")

    @classmethod
    def create(cls, task_id: int, description: str) -> "Task":
        """
        Factory method to create a new task.

        Args:
            task_id: Unique identifier for the task
            description: Task description

        Returns:
            New Task instance

        Raises:
            EmptyDescriptionError: If description is empty or whitespace-only
        """
        return cls(id=task_id, description=description, is_complete=False)
