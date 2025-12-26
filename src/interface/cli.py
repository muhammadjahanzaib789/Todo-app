"""Command-line interface for Todo application."""

from typing import Optional
from src.application.use_cases import (
    AddTaskUseCase,
    ViewTasksUseCase,
    UpdateTaskUseCase,
    DeleteTaskUseCase,
    MarkCompleteUseCase,
    MarkIncompleteUseCase,
)
from src.domain.exceptions import TaskNotFoundError, EmptyDescriptionError


class CLI:
    """Command-line interface for interacting with the Todo application."""

    def __init__(
        self,
        add_task: AddTaskUseCase,
        view_tasks: ViewTasksUseCase,
        update_task: UpdateTaskUseCase,
        delete_task: DeleteTaskUseCase,
        mark_complete: MarkCompleteUseCase,
        mark_incomplete: MarkIncompleteUseCase,
    ) -> None:
        """
        Initialize CLI with use cases.

        Args:
            add_task: Use case for adding tasks
            view_tasks: Use case for viewing tasks
            update_task: Use case for updating tasks
            delete_task: Use case for deleting tasks
            mark_complete: Use case for marking tasks complete
            mark_incomplete: Use case for marking tasks incomplete
        """
        self._add_task = add_task
        self._view_tasks = view_tasks
        self._update_task = update_task
        self._delete_task = delete_task
        self._mark_complete = mark_complete
        self._mark_incomplete = mark_incomplete

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n=== Todo List Application ===\n")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Quit\n")

    def get_user_choice(self) -> str:
        """
        Get menu choice from user.

        Returns:
            User's choice as string
        """
        return input("Enter your choice (1-7): ").strip()

    def get_task_id(self, prompt: str = "Enter task ID: ") -> Optional[int]:
        """
        Get task ID from user with validation.

        Args:
            prompt: Prompt to display

        Returns:
            Task ID as integer, or None if invalid input
        """
        user_input = input(prompt).strip()
        try:
            return int(user_input)
        except ValueError:
            self.display_error("Invalid input format. Please enter a number.")
            return None

    def display_error(self, message: str) -> None:
        """
        Display an error message.

        Args:
            message: Error message to display
        """
        print(f"\n[ERROR] {message}\n")

    def display_success(self, message: str) -> None:
        """
        Display a success message.

        Args:
            message: Success message to display
        """
        print(f"\n[SUCCESS] {message}\n")

    def wait_for_keypress(self) -> None:
        """Wait for user to press Enter."""
        input("[Press Enter to continue...]")

    def handle_add_task(self) -> None:
        """Handle adding a new task."""
        description = input("\nEnter task description: ")

        try:
            task_id = self._add_task.execute(description)
            self.display_success(f"Task added successfully with ID {task_id}.")
        except EmptyDescriptionError:
            self.display_error("Task description cannot be empty. Please provide a description.")

    def handle_view_tasks(self) -> None:
        """Handle viewing all tasks."""
        print("\n=== Task List ===\n")

        tasks = self._view_tasks.execute()

        if not tasks:
            print("No tasks found. Add a task to get started!\n")
        else:
            for task in tasks:
                status = "Complete" if task.is_complete else "Incomplete"
                print(f"[{task.id}] {task.description} - {status}")
            print()

    def handle_update_task(self) -> None:
        """Handle updating a task description."""
        task_id = self.get_task_id("Enter task ID to update: ")
        if task_id is None:
            return

        new_description = input("Enter new description: ")

        try:
            self._update_task.execute(task_id, new_description)
            self.display_success(f"Task {task_id} updated successfully.")
        except TaskNotFoundError:
            self.display_error("Task ID not found. Please check the ID and try again.")
        except EmptyDescriptionError:
            self.display_error("Task description cannot be empty. Please provide a description.")

    def handle_delete_task(self) -> None:
        """Handle deleting a task."""
        task_id = self.get_task_id("Enter task ID to delete: ")
        if task_id is None:
            return

        try:
            self._delete_task.execute(task_id)
            self.display_success(f"Task {task_id} deleted successfully.")
        except TaskNotFoundError:
            self.display_error("Task ID not found. Please check the ID and try again.")

    def handle_mark_complete(self) -> None:
        """Handle marking a task as complete."""
        task_id = self.get_task_id("Enter task ID to mark complete: ")
        if task_id is None:
            return

        try:
            self._mark_complete.execute(task_id)
            self.display_success(f"Task {task_id} marked as complete.")
        except TaskNotFoundError:
            self.display_error("Task ID not found. Please check the ID and try again.")

    def handle_mark_incomplete(self) -> None:
        """Handle marking a task as incomplete."""
        task_id = self.get_task_id("Enter task ID to mark incomplete: ")
        if task_id is None:
            return

        try:
            self._mark_incomplete.execute(task_id)
            self.display_success(f"Task {task_id} marked as incomplete.")
        except TaskNotFoundError:
            self.display_error("Task ID not found. Please check the ID and try again.")

    def handle_invalid_choice(self) -> None:
        """Handle invalid menu choice."""
        self.display_error("Invalid choice. Please enter a number between 1 and 7.")

    def handle_quit(self) -> None:
        """Handle application quit."""
        print("\nGoodbye! Your tasks will not be saved.\n")
