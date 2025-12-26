"""Storage interface for task persistence."""

from abc import ABC, abstractmethod
from typing import Optional


class TaskStorage(ABC):
    """Abstract interface for task storage operations."""

    @abstractmethod
    def save(self, task: "Task") -> int:  # type: ignore
        """Save a task and return its ID."""
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional["Task"]:  # type: ignore
        """Find a task by its ID, return None if not found."""
        pass

    @abstractmethod
    def find_all(self) -> list["Task"]:  # type: ignore
        """Return all tasks."""
        pass

    @abstractmethod
    def update(self, task: "Task") -> None:  # type: ignore
        """Update an existing task."""
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        """Delete a task by its ID."""
        pass
