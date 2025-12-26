"""Use cases - business workflows."""

from src.application.storage import TaskStorage
from src.domain.task import Task
from src.domain.exceptions import TaskNotFoundError, EmptyDescriptionError


class AddTaskUseCase:
    """Use case for adding a new task."""

    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize use case with storage.

        Args:
            storage: Task storage implementation
        """
        self._storage = storage

    def execute(self, description: str) -> int:
        """
        Add a new task with the given description.

        Args:
            description: Task description

        Returns:
            ID of the newly created task

        Raises:
            EmptyDescriptionError: If description is empty
        """
        # Create task with temporary ID 0 (storage will assign real ID)
        task = Task.create(task_id=0, description=description)
        return self._storage.save(task)


class ViewTasksUseCase:
    """Use case for viewing all tasks."""

    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize use case with storage.

        Args:
            storage: Task storage implementation
        """
        self._storage = storage

    def execute(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks sorted by ID
        """
        return self._storage.find_all()


class UpdateTaskUseCase:
    """Use case for updating a task description."""

    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize use case with storage.

        Args:
            storage: Task storage implementation
        """
        self._storage = storage

    def execute(self, task_id: int, new_description: str) -> None:
        """
        Update the description of an existing task.

        Args:
            task_id: ID of the task to update
            new_description: New description

        Raises:
            TaskNotFoundError: If task ID not found
            EmptyDescriptionError: If new description is empty
        """
        task = self._storage.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task ID {task_id} not found")

        # Validate new description
        if not new_description or not new_description.strip():
            raise EmptyDescriptionError("Task description cannot be empty")

        # Create updated task
        updated_task = Task(id=task.id, description=new_description, is_complete=task.is_complete)
        self._storage.update(updated_task)


class DeleteTaskUseCase:
    """Use case for deleting a task."""

    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize use case with storage.

        Args:
            storage: Task storage implementation
        """
        self._storage = storage

    def execute(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Raises:
            TaskNotFoundError: If task ID not found
        """
        self._storage.delete(task_id)


class MarkCompleteUseCase:
    """Use case for marking a task as complete."""

    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize use case with storage.

        Args:
            storage: Task storage implementation
        """
        self._storage = storage

    def execute(self, task_id: int) -> None:
        """
        Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete

        Raises:
            TaskNotFoundError: If task ID not found
        """
        task = self._storage.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task ID {task_id} not found")

        updated_task = Task(id=task.id, description=task.description, is_complete=True)
        self._storage.update(updated_task)


class MarkIncompleteUseCase:
    """Use case for marking a task as incomplete."""

    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize use case with storage.

        Args:
            storage: Task storage implementation
        """
        self._storage = storage

    def execute(self, task_id: int) -> None:
        """
        Mark a task as incomplete.

        Args:
            task_id: ID of the task to mark incomplete

        Raises:
            TaskNotFoundError: If task ID not found
        """
        task = self._storage.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task ID {task_id} not found")

        updated_task = Task(id=task.id, description=task.description, is_complete=False)
        self._storage.update(updated_task)
