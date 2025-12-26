"""Main application entry point."""

from src.infrastructure.memory_storage import MemoryStorage
from src.application.use_cases import (
    AddTaskUseCase,
    ViewTasksUseCase,
    UpdateTaskUseCase,
    DeleteTaskUseCase,
    MarkCompleteUseCase,
    MarkIncompleteUseCase,
)
from src.interface.cli import CLI


def main() -> None:
    """Run the Todo application."""
    # Initialize storage
    storage = MemoryStorage()

    # Initialize use cases
    add_task = AddTaskUseCase(storage)
    view_tasks = ViewTasksUseCase(storage)
    update_task = UpdateTaskUseCase(storage)
    delete_task = DeleteTaskUseCase(storage)
    mark_complete = MarkCompleteUseCase(storage)
    mark_incomplete = MarkIncompleteUseCase(storage)

    # Initialize CLI
    cli = CLI(
        add_task=add_task,
        view_tasks=view_tasks,
        update_task=update_task,
        delete_task=delete_task,
        mark_complete=mark_complete,
        mark_incomplete=mark_incomplete,
    )

    # Main application loop
    while True:
        cli.display_menu()
        choice = cli.get_user_choice()

        try:
            if choice == "1":
                cli.handle_add_task()
            elif choice == "2":
                cli.handle_view_tasks()
            elif choice == "3":
                cli.handle_update_task()
            elif choice == "4":
                cli.handle_delete_task()
            elif choice == "5":
                cli.handle_mark_complete()
            elif choice == "6":
                cli.handle_mark_incomplete()
            elif choice == "7":
                cli.handle_quit()
                break
            else:
                cli.handle_invalid_choice()
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred: {e}")
            print("Returning to main menu.\n")

        # Wait for user before redisplaying menu (except for quit)
        if choice != "7":
            cli.wait_for_keypress()


if __name__ == "__main__":
    main()
