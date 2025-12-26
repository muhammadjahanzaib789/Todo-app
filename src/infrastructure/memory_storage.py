"""In-memory storage implementation."""

from typing import Optional
from src.application.storage import TaskStorage
from src.domain.task import Task
from src.domain.exceptions import TaskNotFoundError


class MemoryStorage(TaskStorage):
    """
    In-memory task storage using Python dictionary.

    Stores tasks in a dictionary for O(1) lookups by ID.
    Uses an integer counter for auto-incrementing IDs starting from 1.
    """

    def __init__(self) -> None:
        """Initialize empty storage with ID counter starting at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def save(self, task: Task) -> int:
        """
        Save a task to storage.

        If task has no ID (0), assigns a new auto-incremented ID.
        If task has an ID, updates the existing task.

        Args:
            task: Task to save

        Returns:
            The task's ID
        """
        if task.id == 0:
            task_id = self._next_id
            self._next_id += 1
            new_task = Task(id=task_id, description=task.description, is_complete=task.is_complete)
            self._tasks[task_id] = new_task
            return task_id
        else:
            self._tasks[task.id] = task
            return task.id

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find a task by its ID.

        Args:
            task_id: ID of the task to find

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def find_all(self) -> list[Task]:
        """
        Return all tasks sorted by ID.

        Returns:
            List of all tasks in ID order
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update(self, task: Task) -> None:
        """
        Update an existing task.

        Args:
            task: Task with updated data

        Raises:
            TaskNotFoundError: If task ID not found
        """
        if task.id not in self._tasks:
            raise TaskNotFoundError(f"Task ID {task.id} not found")
        self._tasks[task.id] = task

    def delete(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Raises:
            TaskNotFoundError: If task ID not found
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task ID {task_id} not found")
        del self._tasks[task_id]
